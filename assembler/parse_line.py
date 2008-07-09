# parse_line.py

# parse one source line

import operations

class AssemblySyntaxError(Exception):
  def __init__(self, info = None):
    self.info = info

  def __str__(self):
    if self.__doc__ is not None:
      return self.__doc__ % self.info
    else:
      return str(self.info)

class MissingOperationError(AssemblySyntaxError):
  """Syntax error, operation missing"""

class InvalidLabelError(AssemblySyntaxError):
  """Invalid label name (%s)"""

class TooLongLabelError(AssemblySyntaxError):
  """Too long label name (%s)"""

class UnknownOperationError(AssemblySyntaxError):
  """Unknown operation: %s"""

class Line:
  def __init__(self, label, operation, argument):
    self.label, self.operation, self.argument = label, operation, argument
    self.line_number = 0

  def __str__(self):
    return "%3i: (%10s) %4s %s" % (self.line_number, self.label, self.operation, self.argument)

def is_label(s):
  return s.isalnum() and any(ch.isalpha() for ch in s)
  
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


  # check argument
  # no check
  
  return Line(label, operation, argument)
