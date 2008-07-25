from errors import *
from execution import *
from word_parser import *

class VMachine:
  MEMORY_SIZE = 4000
  MAX_BYTE = 64
  POSITIVE_ZERO = [1, 0, 0, 0, 0, 0]

  def __getitem__(self, index):
    """Can raise exception"""
    return self.memory[index]

  def __setitem__(self, index, word):
    """Can raise exception"""
    self.memory[index][:] = word[:]

  @staticmethod
  def mix2dec(word):
    return word[0] * reduce(lambda x,y: (x << 6) | y, word[1:], 0)

  @staticmethod
  def dec2mix(num):
    mask = VMachine.MAX_BYTE - 1  # 1<<6 - 1
    u_num = abs(num)
    return [VMachine.sign(num)] + [ (u_num >> shift) & mask for shift in xrange(24, -1, -6) ]

  @staticmethod
  def sign(x):
    if x >= 0:
      return +1
    else:
      return -1
 
  @staticmethod
  def check_mem_addr(addr):
    return 0 <= addr < VMachine.MEMORY_SIZE

  @staticmethod
  def check_word(word):
    return  len(word) == 6\
            and word[0] in (1, -1)\
            and all([ 0 <= byte < VMachine.MAX_BYTE for byte in word[1:6]])

  def cmp_memory(self, memory_dict):
    """Need for testing"""
    positive_zero = VMachine.POSITIVE_ZERO
    if not isinstance(memory_dict, dict) or \
       any( (i     in memory_dict and self[i] != memory_dict[i]) or
            (i not in memory_dict and self[i] != positive_zero)
            for i in xrange(VMachine.MEMORY_SIZE)):
      return False
    else:
      return True

  def get_cur_word(self):
    return self[self.cur_addr]

  def sort_errors(self):
    self.errors.sort(key = lambda x: x[0]) # sort by line_numbers

  def init_memory(self, memory):
    self.memory = [ self.POSITIVE_ZERO[:] for _ in xrange(self.MEMORY_SIZE)]
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

  def init_stuff(self):
    self.rA = self.POSITIVE_ZERO
    self.rX = self.POSITIVE_ZERO
    self.rI = [self.POSITIVE_ZERO for _ in xrange(7)] # one not used rI[0] :)

    self.cf = 0
    self.of = False

    # self.devices = ...

  def __init__(self, memory, start_address):
    self.errors = []
    self.init_memory(memory)
    self.sort_errors()
    self.init_stuff()
    self.word_parser = WordParser(self)
    self.cur_addr = start_address
    self.halted = False

  def print_state(self, file):
    def word2str(word):
      return reduce(lambda x, y: "%s %02i" % (x, y), word[1:6], "+" if word[0] >= 0 else "-")
    file.write("HLT: %s\n" % self.halted)
    file.write("CA:  %s\n" % self.cur_addr)
    file.write("rA:  %s\n" % word2str(self.rA))
    file.write("rX:  %s\n" % word2str(self.rX))
    for i in xrange(1, 7):
      file.write("rI%i: %s\n" % (i, word2str(self.rI[i])))
    file.write("CF:  ")
    if self.cf == -1:
      file.write("LESS")
    elif self.cf == 0:
      file.write("EQUAL")
    elif self.cf == 1:
      file.write("GREATER")
    else:
      file.write("##ERROR##")
    file.write("\n")
    file.write("OF:  %s\n" % self.of)

  def step(self):
    execute(self)
