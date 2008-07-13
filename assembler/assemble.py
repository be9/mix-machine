# assemble.py

# assemble parsed lines to memory

from symbol_table import *
from operations import *
from memory import Memory

def assemble(lines, symbol_table):
  """Now we need to assemble program"""
  errors = []
  memory = Memory()
  ca = 0 # current address (*)
  for line in lines:
    # all by 10th and 11th rules from Donald Knuth's book
    if is_instruction(line.operation):
      c_code, f_code_default = get_codes(line.operation)

      # (in the future) a_code, i_code, f_code = parse_argument(line, symbol_table)
      try:
        a_part = parse_argument(line, symbol_table)
      except AssemblySyntaxError, err:
        errors.append( (line.line_number, err) )
      else:
        i_code = 0
        f_code = f_code_default
        memory.set_instruction(ca, a_part, i_code, f_code, c_code)
        ca += 1
    elif line.operation == "EQU":
      pass
    elif line.operation == "ORIG":
      ca = parse_argument(line, symbol_table)
    elif line.operation == "CON":
      try:
        memory.set_word(ca, parse_argument(line, symbol_table))
      except AssemblySyntaxError, err:
        errors.append( (line.line_number, err) )
      else:
        ca += 1
    elif line.operation == "ALF":
      # FIX ME
      memory.set_word(ca, 20210054) # 20210054 = "ALFFF" = (+1, 1, 13, 6, 6, 6,)
      ca += 1
    elif line.operation == "END":
      # FIX ME: here we put all CON's which comes from smth like "=3="
      try:
        start_address = parse_argument(line, symbol_table)
      except AssemblySyntaxError, err:
        start_address = None
        errors.append( (line.line_number, err) )
      return (memory, start_address, errors) # assemblying finished
