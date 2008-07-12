# parse_argument.py

# parses third part of line

# Grammar of mix's arguments
# SYMBOL          ::==  string with length from 1 to 10 of digits or alphas (one alpha required)
#                       also special symbols dH, dF, dB - where "d" is digit
# NUMBER          ::==  string with length from 1 to 10 of digits
# DEFINED_SYMBOL  ::==  symbol which was previously defined in source file
# FUTURE_SYMBOL   ::==  symbol which was nextly defined in source file
# CUR_ADDR        ::==  "*"
# LITERAL         ::==  "=" W_EXP "="
# S_EXP           ::==  NUMBER | DEFINED_SYMBOL | CUR_ADDR
# EXP             ::==  ["+" | "-"] S_EXP [ ("+" | "-" | "*" | "/" | "//" | ":") S_EXP]*
# ADR_PART        ::==  "" | EXP | FUTURE_SYMBOL | LITERAL
# IND_PART        ::==  "" | ( "," EXP )
# F_PART          ::==  "" | ( "(" EXP ")" )
# W_EXP           ::==  EXP F_PART [ "," EXP F_PART ]*
# ALF_WORD        ::==  exactly five mix-chars
#
# ARGUMENT        ::== ( ADR_PART IND_PART F_PART ) | # if is_instruction(operation)
#                      W_EXP |                        # if operation in ("EQU", "ORIG", "CON", "END")
#                      ALF_WORD                       # if operation == "ALF"

from operations import *
from errors import *

def parse_argument(line, symbol_table):
  arg = line.argument

  # instruction:  number, any symbol (if this function calles for instruction => all symbols were found yet)
  # directives:   number, defined symbol (and only defined symbols are in labels and local_labels)

  if line.argument is None:
    return 0

  try:
    return int(line.argument)
  except:
    pass

  addr = symbol_table.find(line.argument, line.line_number)
  if addr is not None:
    return addr

  raise InvalidExpressionError(arg)
