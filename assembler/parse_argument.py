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


def parse_argument(s):
  if s is not None:
    return int(s)
  else:
    return 0
