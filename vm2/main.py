import sys
from read_memory import *
from virt_machine import *

def print_errors(errors):
  for error in errors:
    print "%i: %s" % (error[0], error[1])

def main():
  if len(sys.argv) != 2: # 1st - program name, 2nd - input filename
    print ERR_INVALID_ARGS[1]
    return ERR_INVALID_ARGS[0]

  try:
    file_in = open(sys.argv[1], "r")
  except IOError, (errno, strerror):
    print "%s (%s): %s" % (ERR_INVALID_INPUT_FILE[1], sys.argv[1], strerror)
    return ERR_INVALID_INPUT_FILE[0]


  memory, start_address, errors = read_memory(file_in.readlines())
  if len(errors) > 0:
    print ERR_SYNTAX[1]
    print_errors(errors)
    return ERR_SYNTAX[0]


  vmachine = VMachine(memory, start_address)

  vmachine.print_state(sys.stdout)
  while not vmachine.halted and len(vmachine.errors) == 0:
    vmachine.step()
  vmachine.print_state(sys.stdout)
  print vmachine[1]

  if len(vmachine.errors) > 0:
    print ERR_VM_RUN[1]
    print_errors(vmachine.errors)
    return ERR_VM_RUN[0]

# if we executing module
if __name__ == '__main__':
  main()
