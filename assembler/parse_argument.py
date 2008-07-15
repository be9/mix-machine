# parse_argument.py

# parses third part of line

# Grammar of mix's arguments:
# + SYMBOL          ::==  string with length from 1 to 10 of digits or alphas (one alpha required)
# +                       also special symbols dH, dF, dB - where "d" is digit
# + NUMBER          ::==  string with length from 1 to 10 of digits
# + DEFINED_SYMBOL  ::==  symbol which was previously defined in source file
# + FUTURE_SYMBOL   ::==  symbol which was nextly defined in source file
#   ALF_WORD        ::==  exactly five mix-chars in inverted or
#                        less than six mix-chars not in inverted
# + NONE            ::==  can be missed
# + CUR_ADDR        ::==  "*"
# + S_EXP           ::==  NUMBER | DEFINED_SYMBOL | CUR_ADDR
# + EXP             ::==  [ "+" | "-" ] S_EXP [ ( "+" | "-" | "*" | "/" | "//" | ":" ) S_EXP]*
# ~ IND_PART        ::==  NONE | ( "," EXP )
# ~ F_PART          ::==  NONE | ( "(" EXP ")" )
# ~ W_EXP           ::==  EXP F_PART [ "," EXP F_PART ]*
#   LITERAL         ::==  "=" W_EXP "="
#   ADR_PART        ::==  NONE | EXP | FUTURE_SYMBOL | LITERAL
#
#   ARGUMENT        ::== ( ADR_PART IND_PART F_PART ) | # if is_instruction(operation)
#                        W_EXP |                        # if operation in ("EQU", "ORIG", "CON", "END")
#                        ALF_WORD                       # if operation == "ALF"

from math import *
from operations import *
from errors import *
from memory import Memory

def parse_argument(line, symbol_table, cur_addr):
# + EQUAL           ::==  "="
  arg_parser = ArgumentParser(line, symbol_table, cur_addr)
  return arg_parser.parse()

class ArgumentParser:
  unary_ops = "+ -".split(" ")
  unary_func = {
    "+":  lambda x : x,
    "-":  lambda x : -x
  }
  binary_ops = "+ - * / // :".split(" ")
  binary_func = {
    "+":  lambda x,y : x + y,
    "-":  lambda x,y : x - y,
    "*":  lambda x,y : x * y,
    "/":  lambda x,y : x / y,
    "//": lambda x,y : (x * 64**5) / y,
    ":":  lambda x,y : 8*x + y
  }

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
    return self.try_w_exp()
    # return self.try_argument() # not done yet


  def get(self):
    try:
      return self.tokens[self.ct]
    except:
      return None


  def next(self):
    self.ct += 1


  def look(self):
    try:
      return self.tokens[self.ct + 1]
    except:
      return None

  @staticmethod
  def try_any(seq):
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
    return self.try_any(
      (self.try_number, self.try_defined_symbol, self.try_cur_addr)
    )


  def try_exp(self):
    result = 0

    has_unary = False
    if self.get() in self.unary_ops:
      unary = self.unary_func[self.get()]
      has_unary = True
      self.next()
    else:
      unary = lambda x : x # identical function

    s_exp = self.try_s_exp()
    if s_exp is None:
      if has_unary:
        raise "ERROR!"
      else:
        return None
    result = unary(s_exp)

    while True:
      if self.look() not in self.binary_ops:
        break
      self.next()
      binary = self.binary_func[self.get()]
      self.next()
      s_exp = self.try_s_exp()
      if s_exp is None:
        raise "ERROR!"
      result = binary(result, s_exp)

    return result


  def try_ind_part(self):
    if self.get() != ",":
      return 0
    else:
      self.next()
      exp = self.try_exp()
      if exp is None:
        raise "ERROR!"
      else:
        return exp


  def try_f_part(self):
    if self.get() != "(":
      return get_codes(self.line.operation)[1]
    else:
      self.next()
      exp = self.try_exp()
      if exp is None:
        raise "ERROR!"
      else:
        self.next()
        if self.get() != ")":
          raise "ERROR!"
        else:
          return exp


  def try_w_exp(self):
    word = [+1, 0, 0, 0, 0, 0]
    value = self.try_exp()
    if value is None:
      return None

    if self.look() == "(":
      self.next()
      field = self.try_f_part()
    else:
      field = get_codes(self.line.operation)[1]

    if Memory.apply_to_word(value, word, field) is None:
      raise "ERROR!"

    while True:
      if self.look() != ",":
        break

      self.next()
      self.next()

      value = self.try_exp()
      if value is None:
        raise "ERROR!"

      if self.look() == "(":
        self.next()
        field = self.try_f_part()
      else:
        field = get_codes(self.line.operation)[1]

      if Memory.apply_to_word(value, word, field) is None:
        raise "ERROR!"

    return Memory.mix2dec(word)
