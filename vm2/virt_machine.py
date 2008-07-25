from errors import *

MEMORY_SIZE = 4000
MAX_BYTE = 64

class VMachine:
  @staticmethod
  def positive_zero():
    return [1, 0, 0, 0, 0, 0]

  def __getitem__(self, index):
    """Can raise exception"""
    return self.memory[index]

  def __setitem__(self, index, word):
    """Can raise exception"""
    self.memory[index][:] = word[:]

  @staticmethod
  def check_mem_addr(addr):
    return 0 <= addr < MEMORY_SIZE

  @staticmethod
  def check_word(word):
    return  len(word) == 6\
            and word[0] in (1, -1)\
            and all([ 0 <= byte < MAX_BYTE for byte in word[1:6]])

  def cmp_memory(self, memory_dict):
    """Need for testing"""
    positive_zero = self.positive_zero()
    if not isinstance(memory_dict, dict) or \
       any( (i     in memory_dict and self[i] != memory_dict[i]) or
            (i not in memory_dict and self[i] != positive_zero)
            for i in xrange(MEMORY_SIZE)):
      return False
    else:
      return True

  def sort_errors(self):
    self.errors.sort(key = lambda x: x[0]) # sort by line_numbers

  def init_memory(self, memory):
    self.memory = [ self.positive_zero()[:] for _ in xrange(MEMORY_SIZE)]
    for addr, (word, line_number) in memory.items():

      # checking for correct input
      if self.check_mem_addr(addr) and self.check_word(word):
        #all is OK
        self[addr] = word

      else:
        if self.check_mem_addr(addr):
          self.errors.append( (line_number, InvalidMixWordError(tuple(word))) )
        else:
          self.errors.append( (line_number, InvalidMemAddrError(addr)) )


  def __init__(self, memory = None):
    self.errors = []
    self.init_memory(memory if memory is not None else {})
    self.sort_errors()
