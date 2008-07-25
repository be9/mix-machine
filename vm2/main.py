import sys
from read_memory import *

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


# if we executing module
if __name__ == '__main__':
  main()
