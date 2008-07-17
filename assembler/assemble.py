# assemble.py

# assemble parsed lines to memory

import operations
from errors import AssemblySyntaxError
from parse_argument import parse_argument
from memory import Memory

class Assembler:
  def __init__(self, symtable):
    self.memory = Memory()
    self.symtable = symtable

  def run(self, lines):
    self.start_address = None
    self.ca = 0
    self.errors = []

    for line in lines:
      try:
        if operations.is_instruction(line.operation):
          self.do_instruction(line)
        else:
          Assembler.__dict__["do_" + line.operation.lower()](self, line)

      except AssemblySyntaxError, err:
        self.errors.append( (line.line_number, err) )
  
  def do_instruction(self, line):
    word_value = self._parse_arg(line)
    
    c_code = operations.get_codes(line.operation)[0]
    self._write_word((abs(word_value) | c_code) * Memory.sign(word_value))

  def do_equ(self, line):
    pass

  def do_orig(self, line):
    self.ca = parse_argument(line, self.symtable, self.ca)
    
  def do_con(self, line):
    self._write_word(self._parse_arg(line))

  do_alf = do_con

  def do_end(self, line):
    self.start_address = self._parse_arg(line)
    assert(self.ca, self.symtable.end_address)

    for value in self.symtable.literals:
      if self.ca >= 4000:
        raise NoFreeSpaceForLiteralsError

      self._write_word(value)

  def _parse_arg(self, line):
    return parse_argument(line, self.symtable, self.ca)

  def _write_word(self, word):
    self.memory[self.ca] = word
    self.ca += 1

def assemble(lines, symbol_table):
  asm = Assembler(symbol_table)
  asm.run(lines)

  return (asm.memory, asm.start_address, asm.errors) # assemblying finished
