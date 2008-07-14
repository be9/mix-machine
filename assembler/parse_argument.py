# parse_argument.py

# parses third part of line

# Grammar of mix's arguments:
#+SYMBOL          ::==  string with length from 1 to 10 of digits or alphas (one alpha required)
#+                       also special symbols dH, dF, dB - where "d" is digit
#+NUMBER          ::==  string with length from 1 to 10 of digits
#+DEFINED_SYMBOL  ::==  symbol which was previously defined in source file
#+FUTURE_SYMBOL   ::==  symbol which was nextly defined in source file
# ALF_WORD        ::==  exactly five mix-chars in inverted or
#                       less than six mix-chars not in inverted
# NONE            ::==  ""
#+CUR_ADDR        ::==  "*"
# EQUAL_SIGN      ::==  "="
# COMMA           ::==  ","
# L_BRACKET       ::==  "("
# R_BRACKET       ::==  ")"
# UNARY_OP        ::==  "+" | "-"
# BINARY_OP       ::==  "+" | "-" | "*" | "/" | "//" | ":"
# LITERAL         ::==  EQUAL_SIGN W_EXP EQUAL_SIGN
#+S_EXP           ::==  NUMBER | DEFINED_SYMBOL | CUR_ADDR
# EXP             ::==  UNARY_OP S_EXP [ BINARY_OP S_EXP]*
# ADR_PART        ::==  NONE | EXP | FUTURE_SYMBOL | LITERAL
# IND_PART        ::==  NONE | ( COMMA EXP )
# F_PART          ::==  NONE | ( L_BRACKET EXP R_BRACKET )
# W_EXP           ::==  EXP F_PART [ COMMA EXP F_PART ]*
#
# ARGUMENT        ::== ( ADR_PART IND_PART F_PART ) | # if is_instruction(operation)
#                      W_EXP |                        # if operation in ("EQU", "ORIG", "CON", "END")
#                      ALF_WORD                       # if operation == "ALF"

from operations import *
from errors import *

def parse_argument(line, symbol_table, cur_addr):
  arg_parser = ArgumentParser(line, symbol_table, cur_addr)
  return arg_parser.parse()

class ArgumentParser:
  def __init__(self, line, symbol_table, cur_addr):
    self.line = line
    self.symbol_table = symbol_table
    self.cur_addr = cur_addr
    self.split() # create self.tokens and ct=0 (current token)


  def split(self):
    self.tokens = []
    self.ct = 0 # current token
    s = self.line.argument
    if s is None:
      return
    splitters = ", + - * / : ( ) \" =".split(" ")
    cur_token = ""
    i = 0
    while i < len(s):
      if s[i] not in splitters:
        cur_token += s[i]
      else:
        if cur_token != "": 
          self.tokens.append(cur_token)
        cur_token = ""
        if s[i] == "/" and i + 1 < len(s) and s[i+1] == "/":
          self.tokens.append("//")
          i += 1
        else:
          self.tokens.append(s[i])
      i += 1
    if cur_token != "":
      self.tokens += [cur_token]


  def parse(self):
    return self.try_s_exp()
    # return self.try_argument() # not done yet


  def get(self):
    # FIX ME: errors
    try:
      return self.tokens[self.ct]
    except:
      return None


  def next(self):
    self.ct += 1


  def look(self):
    return self.tokens[self.ct + 1]

  @staticmethod
  def try_them(seq):
    for f in (seq):
      res = f()
      if res is not None:
        return res
    return None

# all try_*() returns number or None if fails
# and only few raises exceptions

  def try_symbol(self):
    if self.get() is not None:
      return self.symbol_table.find(self.get(), self.line.line_number)
    else:
      return None


  def try_number(self):
    if self.get() is not None and 1 <= len(self.get()) <= 10 and self.get().isdigit():
      return int(self.get())
    else:
      return None


  def try_defined_symbol(self):   # Program algorithm is so that difference of symbols destroied.
    return self.try_symbol()      # Init of symbol table - there parsed arguments of directives
                                  # which use only DEFINED_SYMBOLS with symbol table that created
                                  # from defined labels (see algorithm).
  def try_future_symbol(self):    # Assemble - there parsed arguments of instructions
    return self.try_symbol()      # which use any symbols with full symbol table.


  def try_cur_addr(self):
    if self.get() == "*":
      return self.cur_addr
    else:
      return None

  def try_s_exp(self):
    return self.try_them(
      (self.try_number, self.try_defined_symbol, self.try_cur_addr)
    )
