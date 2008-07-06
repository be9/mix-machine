class Line:
  def __init__(self):
    self.label = None
    self.mnemonic = None
    self.operand = None

# returns Line object or None if text_line is empty
def parse(text_line):
  # ignore comments and whitespace lines
  if len(text_line.strip()) == 0 or text_line[0] == '*':
    return None

  # FIXME
  return Line()
