# parse_line.py

# parse one source line

import mnemonics

class AssemblySyntaxError(Exception):
  def __init__(self, info = None):
    self.info = info

  def __str__(self):
    if self.__doc__ is not None:
      return self.__doc__ % self.info
    else:
      return str(self.info)

class MissingMnemonicError(AssemblySyntaxError):
  """Syntax error, mnemonic missing"""

class InvalidLabelError(AssemblySyntaxError):
  """Invalid label name (%s)"""

class TooLongLabelError(AssemblySyntaxError):
  """Too long label name (%s)"""
    
class UnknownMnemonicError(AssemblySyntaxError):
  """Unknown mnemonic: %s"""

class MissingOperandError(AssemblySyntaxError):
  """Missing operand for %s"""
    
class Line:
  def __init__(self, label, mnemonic, operand):
    self.label, self.mnemonic, self.operand = label, mnemonic, operand
    self.line_number = 0

  def __str__(self):
    return "%3i: (%10s) %4s %s" % (self.line_number, self.label, self.mnemonic, self.operand)

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
    raise MissingMnemonicError

  # line without an operand
  if len(split_line) < 3:
    split_line.append(None)

  label, mnemonic, operand = split_line[0:3]
  
  # check label
  if label is not None:
    if not is_label(label):
      raise InvalidLabelError(label)
    
    if len(label) > 10:
      raise TooLongLabelError(label)
   
  # check mnemonic 
  if not mnemonics.is_valid_mnemonic(mnemonic):
    raise UnknownMnemonicError(mnemonic)

  # check operand
  if operand is None and mnemonics.must_have_operand(mnemonic):
    raise MissingOperandError(mnemonic)
  
  return Line(label, mnemonic, operand)
