# parse_line.py

# parse one source line

import mnemonics

class AssemblySyntaxError(Exception): pass

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
  if not text_line[0].isalnum():
    split_line.insert(0, None)

  if len(split_line) < 2:
    raise AssemblySyntaxError('Syntax error, mnemonics missing')

  # line without an operand
  if len(split_line) < 3:
    split_line.append(None)

  label, mnemonic, operand = split_line[0:3]
  
  # check label
  if label is not None:
    if not is_label(label):
      raise AssemblySyntaxError('Invalid name "%s" for label' % label)
    
    if len(label) > 10:
      raise AssemblySyntaxError('Very long name "%s" for label' % label)
   
  # check mnemonic 
  if not mnemonics.is_valid_mnemonic(mnemonic):
    raise AssemblySyntaxError('Unknown mnemonic "%s"' % mnemonic)

  # check operand
  if operand is None and mnemonics.must_have_operand(mnemonic):
    raise AssemblySyntaxError('No operand for "%s"' % mnemonic)
  
  return Line(label, mnemonic, operand)
