from parse_line import Line

class ListingLine:
  def __init__(self, addr = None, word = None, line = None):
    self.addr = addr
    self.word = word
    self.line = line

  @staticmethod
  def _addr2str(addr):
    if addr is not None:
      return str(addr)
    else:
      return ""

  @staticmethod
  def _word2str(word):
    if word is not None:
      sign = "+" if word[0] == 1 else "-"
      return "%s %02i %02i %02i %02i %02i" % tuple([sign] + word[1:])
    else:
      return ""

  def __str__(self):
    return "%4s | %16s | %s" % (self._addr2str(self.addr), self._word2str(self.word), self.line)

  def __cmp__(self, other):
    if self.addr != other.addr or self.word != other.word or self.line != other.line:
      return 1
    else:
      return 0

class Listing:
  def __str__(self):
    return reduce(lambda x,y: x + str(y) + '\n', self.lines, "")

  def __init__(self, src_lines, asm_lines, memory, literals, literals_address):
    # None added: so first line will have index 1
    self.lines = map(lambda string: ListingLine(line = string.rstrip('\r\n')), src_lines)
    self.asm_lines = asm_lines
    self.memory = memory
    self.literals = literals
    self.literals_address = literals_address
    self.create_listing()

  def create_listing(self):
    for asm_line in self.asm_lines:
      if asm_line.asm_address is not None:
        self.lines[asm_line.line_number-1].addr = asm_line.asm_address
        self.lines[asm_line.line_number-1].word = self.memory[asm_line.asm_address]
    for literal in self.literals:
      sign = "-" if literal[1] == -1 else ""
      self.lines.append(ListingLine(self.literals_address,  self.memory[self.literals_address], "\tCON\t%s%i" % (sign, literal[0])))
      self.literals_address += 1
