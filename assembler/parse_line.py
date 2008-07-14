# parse_line.py

# parse one source line

import operations
from errors import *
from symbol_table import *

class Line:
  def __init__(self, label, operation, argument, line_number = 0):
    self.label, self.operation, self.argument, self.line_number = label, operation, argument, line_number

  def __str__(self):
    return "%3i: (%10s) %4s %s" % (self.line_number, self.label, self.operation, self.argument)

  def __cmp__(self, another):
    """ Mostly needed for tests """
    return cmp(self.__str__(), another.__str__())

# returns Line object or None if text_line is empty or comment line
def parse_line(text_line):
  split_line = text_line.upper().split()

  # empty line or comment line
  if len(split_line) == 0 or text_line[0] == '*':
    return None

  # line without a label
  if text_line[0].isspace():
    split_line.insert(0, None)

  if len(split_line) < 2:
    raise MissingOperationError

  # line without an operand
  if len(split_line) < 3:
    split_line.append(None)

  label, operation, argument = split_line[0:3]

  # check label
  if label is not None:
    if not is_label(label):
      raise InvalidLabelError(label)
    
    if len(label) > 10:
      raise TooLongLabelError(label)
   
  # check operation 
  if not operations.is_valid_operation(operation):
    raise UnknownOperationError(operation)
  
  # check arg for directives
  if operations.is_arg_required(operation) and argument is None:
    raise ArgumentRequiredError(operation)

  return Line(label, operation, argument)

def parse_lines(lines):
  errors = []           # array for (line_numbers, error_messages)
  result = []

  has_end = False
  for i in xrange(len(lines)):
    try:
      line = parse_line(lines[i])
    except AssemblySyntaxError, error:
      errors.append( (i + 1, error) )
    else:
      if line is not None:
        line.line_number = i + 1
        result.append(line)
        if line.operation == "END":
          has_end = True
          break

  if not has_end:
    errors.append( (len(lines), NoEndError()) )

  return (result, errors)
