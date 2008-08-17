import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'assembler'))

from parse_line import *
from assemble import *
from listing import *
#from errors import *

# types of returning value
ASM_NO_ERRORS =         0
ASM_SYNTAX_ERRORS =     1
ASM_ASSEMBLER_ERRORS =  2

class AsmData:
  def __init__(self, mem_list, start_addr, listing):
    self.mem_list = mem_list
    self.start_addr = start_addr
    self.listing = listing

def asm(text):
  src_lines = text.splitlines()

  lines, errors = parse_lines(src_lines)
  if len(errors) > 0: # we have errors
    return (ASM_SYNTAX_ERRORS, errors)

  asm = Assembler()
  asm.run(lines)

  memory_list = asm.memory.memory
  start_address = asm.start_address
  errors = asm.errors

  if len(errors) > 0: # we have errors
    return (ASM_ASSEMBLER_ERRORS, errors)

  listing = Listing(src_lines, lines, memory_list, asm.symtable.literals, asm.end_address)

  return (ASM_NO_ERRORS, AsmData(memory_list, start_address, listing))