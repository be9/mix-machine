# parse_lines.py

# read array of lines from file

from parse_line import *
from errors import *

def parse_lines(lines):
  errors = list() # array for (line_numbers, error_messages)
  result = list()
  for i in xrange(len(lines)):
    try:
      line = parse_line(lines[i])
    except AssemblySyntaxError, error:
      errors.append( (i + 1, error) )
      continue
    if(line is None):
      continue
    line.line_number = i + 1
    result.append(line)
  return (result, errors)
