from errors import *

# input format:
# required FIRST line - start address
# than goes any number of lines like "xxxx: +/-1 xx xx xx xx xx" - any other lines ignored

def parse_word(line):
  """Returns tuple of word index and list like [+1, 0, 0, 0, 0, 0]"""
  # FIX ME
  return (10, [+1, 1, 1, 1, 1, 1])

def read_memory(lines):
  errors = []

  try:
    start_address = int(lines[0])
  except ValueError:
    errors.append( (0, InvalidStartAddressError(lines[0])) )
    return (None, None,  errors)
  except IndexError:
    errors.append( (0, InvalidStartAddressError("")) )
    return (None, None, errors)

  
  return (None, start_address, errors)