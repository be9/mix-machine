# parse_argument.py

# parses third part of line

# Grammar of mix's arguments
# SYMBOL          ::==  string with length from 1 to 10 of digits or alphas (one alpha required)
#                       also special symbols dH, dF, dB - where "d" is digit
# NUMBER          ::==  string with length from 1 to 10 of digits
# DEFINED_SYMBOL  ::==  symbol which was previously defined in source file
# FUTURE_SYMBOL   ::==  symbol which was nextly defined in source file
# NONE            ::==  ""
# CUR_ADDR        ::==  "*"
# LITERAL         ::==  "=" W_EXP "="
# S_EXP           ::==  NUMBER | DEFINED_SYMBOL | CUR_ADDR
# EXP             ::==  ["+" | "-"] S_EXP [ ("+" | "-" | "*" | "/" | "//" | ":") S_EXP]*
# ADR_PART        ::==  NONE | EXP | FUTURE_SYMBOL | LITERAL
# IND_PART        ::==  NONE | ( "," EXP )
# F_PART          ::==  NONE | ( "(" EXP ")" )
# W_EXP           ::==  EXP F_PART [ "," EXP F_PART ]*
# ALF_WORD        ::==  exactly five mix-chars in inverted or
#                       less than six mix-chars not in inverted
#
# ARGUMENT        ::== ( ADR_PART IND_PART F_PART ) | # if is_instruction(operation)
#                      W_EXP |                        # if operation in ("EQU", "ORIG", "CON", "END")
#                      ALF_WORD                       # if operation == "ALF"

from operations import *
from errors import *

def parse_argument(line, symbol_table):
  arg_parser = ArgumentParser(line, symbol_table)
  return arg_parser.parse()

class ArgumentParser:
  def __init__(self, line, symbol_table):
    self.line = line
    self.symbol_table = symbol_table
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
    return self.try_symbol()
    # return self.try_argument() # not done yet


  def get(self):
    # FIX ME: errors
    return self.tokens[self.ct]


  def next(self):
    self.ct += 1


  def look(self):
    return self.tokens[self.ct + 1]


# all try_*() returns number or None if fails
# and only few raises exceptions

  def try_symbol(self):
    return self.symbol_table.find(self.get(), self.line.line_number)
