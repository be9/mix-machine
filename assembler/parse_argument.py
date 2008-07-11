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

def parse_argument(line, labels, local_labels):
  arg = line.argument

  # instruction:  number, any symbol (if this function calles for instruction => all symbols were found yet)
  # directives:   number, defined symbol (and only defined symbols are in labels and local_labels)

  if arg is None:
    return 0

  try:
    return int(arg)
  except:
    pass

  # it's SYMBOL

  # find in labels
  if arg in labels:
    return labels[arg]

  # find in local_labels
  if len(arg) == 2 and arg[0].isdigit() and arg[1] in ('F', 'B'):
    label = arg[0] + 'H'
    if label in local_labels:

      b_label, f_label = None, None
      for x in local_labels[label]:
        if x[1] < line.line_number:
          b_label = x
        if x[1] > line.line_number:
          f_label = x
          break

      if arg[1] == 'B' and b_label is not None:
        return b_label[0]
      elif arg[1] == 'F' and f_label is not None:
        return f_label[0]

    raise InvalidLocalLabelError(line.argument)

  raise InvalidExpressionError(arg)