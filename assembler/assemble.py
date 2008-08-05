# assemble.py

# assemble parsed lines to memory

import operations
from errors import *
from parse_argument import parse_argument
from memory import Memory
from symbol_table import SymbolTable

class Assembler:
  def __init__(self, symtable = None):
    self.memory = Memory()
    self.symtable = SymbolTable() if symtable is None else symtable
    self.end_address = None

  def run(self, lines, only = None):
    self.start_address = None
    self.errors = []
    self.error_set = set()

    if only != 2:
      self.ca, self.npass = 0, 1
      self._do_pass(lines)

    if only != 1:
      self.ca, self.npass = 0, 2
      self.symtable.literal_address = self.end_address
      self.occupied_cells = []
      self._do_pass(lines)

  def _do_pass(self, lines):
    for line in lines:
      try:
        if self.npass == 1 and line.operation != "EQU": 
          self._add_label(line)

        if operations.is_instruction(line.operation):
          self._do_instruction(line)
        else:
          Assembler.__dict__["_do_" + line.operation.lower()](self, line)

      except AssemblyError, err:
        self._add_error(line, err)

  def _do_instruction(self, line):
    self._check_address(line)
        
    if self.npass == 1:
      # first pass
      try:
        self._parse_arg(line)
      except AssemblyError:
        # errors in parsing argument are checked on the 2nd pass
        pass
      
      self.ca += 1
    else:
      # second pass
      value, sign = self._parse_arg(line)
      
      c_code = operations.get_codes(line.operation)[0]
      self._write_word( value | c_code, sign )

  def _do_equ(self, line):
    if self.npass == 1:
      self.symtable.set_label(line.label, self._parse_arg(line)[0], line.line_number)

  def _do_orig(self, line):
    self.ca = self._parse_arg(line)[0]
    self._check_address(line)
    
  def _do_con(self, line):
    self._check_address(line)
    
    if self.npass == 2:
      value, sign = self._parse_arg(line)
      self._write_word(value, sign)
    else:
      self.ca += 1

  _do_alf = _do_con

  def _do_end(self, line):
    if self.npass == 1:
      self.end_address = self.ca

    if self.npass == 2:
      self.start_address = self._parse_arg(line)[0]

      for value in self.symtable.literals:
        if not self.memory.is_valid_address(self.ca):
          raise NoFreeSpaceForLiteralsError

        self._write_word(value)

  def _parse_arg(self, line):
    return parse_argument(line, self.symtable, self.ca, self.npass)

  def _write_word(self, value, sign = None):
    if sign is not None:
      real_sign = sign
    else:
      real_sign = +1 if value >= 0 else -1
    if self.ca in self.occupied_cells:
      raise RepeatedCellError(self.ca)
    else:
      self.occupied_cells.append(self.ca)
      self.memory[self.ca] = value
      self.memory.set_sign(self.ca, real_sign)
      self.ca += 1

  def _add_error(self, line, error):
    # do not allow two errors of the same type in one line
    error_tuple = (line.line_number, error.__class__)

    if error_tuple not in self.error_set:
      self.errors.append( (line.line_number, error) )
      self.error_set.add(error_tuple)

  def _add_label(self, line):
    if line.label is not None:
      try:
          self.symtable.set_label(line.label, self.ca, line.line_number)
      except AssemblyError, err:
        self._add_error(line, err)

  def _check_address(self, line):
    if self.npass == 1 and not self.memory.is_valid_address(self.ca):
      self._add_error(line, LineNumberError(self.ca))
