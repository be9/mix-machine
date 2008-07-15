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
# + EQUAL           ::==  "="
# + COMMA           ::==  ","
# + L_BRACKET       ::==  "("
# + R_BRACKET       ::==  ")"
# + UPLUS           ::==  "+"
# + UMINUS          ::==  "-"
# + PLUS            ::==  "+"
# + MINUS           ::==  "-"
# + MULT            ::==  "*"
# + DIV             ::==  "/"
# + FDIV            ::==  "//"
# + COLON           ::==  ":"
# + UNARY_OP        ::==  UPLUS | UMINUS
# + BINARY_OP       ::==  PLUS | MINUS | MULT | DIV | FDIV | COLON
# + S_EXP           ::==  NUMBER | DEFINED_SYMBOL | CUR_ADDR
# + EXP             ::==  [ UNARY_OP ] S_EXP [ BINARY_OP S_EXP]*
# ~ IND_PART        ::==  NONE | ( COMMA EXP )
# ~ F_PART          ::==  NONE | ( L_BRACKET EXP R_BRACKET )
# ~ W_EXP           ::==  EXP F_PART [ COMMA EXP F_PART ]*
#   LITERAL         ::==  EQUAL W_EXP EQUAL
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
    return self.try_w_exp()
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


  def try_equal(self):
    if self.get() == "=":
      return True
    else:
      return None


  def try_comma(self):
    if self.get() == ",":
      return True
    else:
      return None


  def try_l_bracket(self):
    if self.get() == "(":
      return True
    else:
      return None


  def try_r_bracket(self):
    if self.get() == ")":
      return True
    else:
      return None


  def try_cur_addr(self):
    if self.get() == "*":
      return self.cur_addr
    else:
      return None


  def try_uplus(self):
    if self.get() == "+":
      return lambda x : x
    else:
      return None


  def try_uminus(self):
    if self.get() == "-":
      return lambda x : -x
    else:
      return None


  def try_plus(self):
    if self.get() == "+":
      return lambda x,y : x + y
    else:
      return None


  def try_minus(self):
    if self.get() == "-":
      return lambda x,y : x - y
    else:
      return None


  def try_mult(self):
    if self.get() == "*":
      return lambda x,y : x * y
    else:
      return None


  def try_div(self):
    if self.get() == "/":
      return lambda x,y : x / y
    else:
      return None


  def try_fdiv(self):
    if self.get() == "//":
      return lambda x,y : (x * 64**5) / y
    else:
      return None


  def try_colon(self):
    if self.get() == "-":
      return lambda x,y : 8*x + y
    else:
      return None


  def try_unary_op(self):
    return self.try_any(
      (self.try_uplus, self.try_uminus)
    )


  def try_binary_op(self):
    return self.try_any(
      (self.try_plus, self.try_minus, self.try_mult, self.try_div, self.try_fdiv, self.try_colon)
    )


  def try_s_exp(self):
    return self.try_any(
      (self.try_number, self.try_defined_symbol, self.try_cur_addr)
    )


  def try_exp(self):
    result = 0
    unary = self.try_unary_op()
    if unary is not None:
      self.next()
    else:
      unary = lambda x : x

    s_exp = self.try_s_exp()
    if s_exp is None:
      if unary is None:
        return None
      else:
        raise "ERROR!"
    result = unary(s_exp)

    while True:
      self.next()
      binary = self.try_binary_op()
      if binary is None:
        break
      else:
        self.next()
        s_exp = self.try_s_exp()
        if s_exp is None:
          raise "ERROR!"
        result = binary(result, s_exp)

    return result


  def try_ind_part(self):
    if self.try_comma() is None:
      return 0
    else:
      self.next()
      exp = self.try_exp()
      if exp is None:
        raise "ERROR!"
      else:
        return exp


  def try_f_part(self):
    if self.try_l_bracket() is None:
      field = get_codes(self.line.operation)[1]
      if field is not None:
        return field
      else:
        return 5
    else:
      self.next()
      exp = self.try_exp()
      if exp is None:
        raise "ERROR!"
      else:
        self.next()
        if self.try_r_bracket() is None:
          raise "ERROR!"
        else:
          return exp


  def try_w_exp(self):
    print "--------------------"
    word = [+1, 0, 0, 0, 0, 0]
    print self.ct
    value = self.try_exp()
    print self.ct
    print "VALUE:", value
    if value is None:
      return None
    self.next()
    print self.tokens[self.ct-1:self.ct+2]
    field = self.try_f_part()
    print "FIELD:", field
    self.next()
    if Memory.apply_to_word(value, word, field) is None:
      raise "ERROR!"
    print "WORD:", word
    while True:
      if self.try_comma() is None:
        break
      self.next()
      value = self.try_exp()
      print "VALUE:", value
      if value is None:
        raise "ERROR!"
      self.next()
      field = self.try_f_part()
      print "FIELD:", field
      if field is None:
        raise "ERROR!"
      self.next()
      if Memory.apply_to_word(value, word, field) is None:
        raise "ERROR!"
      print "WORD:", word
    return Memory.mix2dec(word)
