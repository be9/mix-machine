from errors import *

# input format:
# required FIRST line - start address
# than goes any number of lines like "xxxx +/-1 xx xx xx xx xx [comment]" or empty lines


def parse_word(line):
  """Returns tuple of word index and list like [+1, 0, 0, 0, 0, 0] or None if empty line"""
  if len(line.rstrip()) == 0:
    return None
  parts = line.split()
  if len(parts) < 7:
    raise TooShortInputLineError(line)
  numbers = []
  # map(..., ...) not used for catching errors
  for s in parts[:7]:
    try:
      numbers.append(int(s))
    except ValueError:
      raise InvalidIntError(s)
  return (numbers[0], numbers[1:7])

def read_memory(lines):
  errors = []
  try:
    start_address = int(lines[0])
  except ValueError:
    start_address = None
    errors.append(  (1, InvalidStartAddressError(lines[0].rstrip())) )
  except IndexError:
    start_address = None
    errors.append( (1, InvalidStartAddressError("")) )

  memory = {}
  for i in xrange(1, len(lines)):
    try:
      res = parse_word(lines[i])
    except VMError, e:
      errors.append( (i + 1, e) )
    else:
      if res is None:
        continue
      else:
        if res[0] in memory:
          errors.append( (i + 1, RepeatedAddressError(res[0])) )
        else:
          memory[res[0]] = (res[1], i + 1)

  return (memory, start_address, errors)