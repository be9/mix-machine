# main.py

# Assembler - one of the parts of MixMachine,
# which assemles mix source code ("*.mix") to
# Mix Assembled code ("*.ma")

# Main module of assembler.
# Read two file names (gets by command line arguments):
# 1) input file (required)
# 2) output file (default "out.ma")

import sys
from errors import *
from parse_line import *
from assemble import *
from memory import Memory

DEFAULT_OUT_NAME = "out.ma"

def print_errors(errors):
  for error in errors:
    print "%04i: %s" % (error[0], error[1])

def write_memory(file, memory):
  for i in xrange(len(memory)):
    if memory[i] != Memory.positive_zero():
      file.write("%04i: %+2i %02i %02i %02i %02i %02i\n" % tuple([i] + memory[i]))

def write_asm_file(file, start_address, memory):
  file.write("%i\n" % start_address)
  write_memory(file, memory)

def main():
  arg_number = len(sys.argv) - 1
  if arg_number < 1 or arg_number > 2:
    print ERR_INVALID_ARGS[1]
    return ERR_INVALID_ARGS[0]

  try:
    file_in = open(sys.argv[1], "r")
  except IOError, (errno, strerror):
    print "%s (%s): %s" % (ERR_INVALID_INPUT_FILE[1], sys.argv[1], strerror)
    return ERR_INVALID_INPUT_FILE[0]

  try:
    file_out = open(sys.argv[2] if arg_number == 2 else DEFAULT_OUT_NAME, 'w')
  except IOError, (errno, strerror):
    file_in.close()
    print "%s (%s): %s" % (ERR_INVALID_OUTPUT_FILE[1],
                           sys.argv[2] if arg_number == 2 else DEFAULT_OUT_NAME,
                           strerror)
    return ERR_INVALID_OUTPUT_FILE[0]


  lines, errors = parse_lines(file_in.readlines())
  file_in.close()
  if len(errors) > 0: # we have errors
    print "Syntax errors:"
    print_errors(errors)
    file_out.close()
    return ERR_SYNTAX[0]

  asm = Assembler()
  asm.run(lines)

  memory_table = asm.memory
  start_address = asm.start_address
  errors = asm.errors


  if len(errors) > 0: # we have errors
    print "Assemble errors:"
    print_errors(errors)
    file_out.close()
    return ERR_ASSEMBLE[0]

  if start_address is not None:
    print "Start address: %04i" % start_address
  if memory_table is not None:
    print "Memory:"
    write_memory(sys.stdout, memory_table.memory)

  write_asm_file(file_out, start_address, memory_table.memory)
  file_out.close()
	
# if we executing module
if __name__ == '__main__':
  main()
