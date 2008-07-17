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
      try:
        word_value = parse_argument(line, symbol_table, ca)
      except AssemblySyntaxError, err:
        errors.append( (line.line_number, err) )
      else:
        c_code = get_codes(line.operation)[0]
        word_value = (abs(word_value) | c_code) * Memory.sign(word_value)
        memory[ca] = word_value
        ca += 1
    elif line.operation == "EQU":
      pass
    elif line.operation == "ORIG":
      ca = parse_argument(line, symbol_table, ca)
    elif line.operation == "CON":
      try:
        memory[ca] = parse_argument(line, symbol_table, ca)
      except AssemblySyntaxError, err:
        errors.append( (line.line_number, err) )
      else:
        ca += 1
    elif line.operation == "ALF":
      try:
        memory[ca] = parse_argument(line, symbol_table, ca)
      except AssemblySyntaxError, err:
        errors.append( (line.line_number, err) )
      else:
        ca += 1
    elif line.operation == "END":
      # FIX ME: here we put all CON's which comes from smth like "=3="
      try:
        start_address = parse_argument(line, symbol_table, ca)
      except AssemblySyntaxError, err:
        start_address = None
        errors.append( (line.line_number, err) )
      else:
        # now ca must be equal to symbol_table.end_address
        assert(ca, symbol_table.end_address)
        for value in symbol_table.literals:
          if ca >= 4000:
            errors.append( (line.line_number, NoFreeSpaceForLiteralsError()) )
            break
          memory[ca] = value
          ca += 1
      return (memory, start_address, errors) # assemblying finished
