from errors import *
from execution import *
from word_parser import *
from word import *

class VMachine:
  MEMORY_SIZE = 4000

  def __getitem__(self, index):
    """Can raise exception"""
    return self.memory[index]

  def __setitem__(self, index, word):
    """Can raise exception"""
    self.memory[index][:] = word[:]
 
  @staticmethod
  def check_mem_addr(addr):
    return 0 <= addr < VMachine.MEMORY_SIZE

  def cmp_memory(self, memory_dict):
    """Need for testing"""
    positive_zero = Word()
    if not isinstance(memory_dict, dict) or \
       any( (i     in memory_dict and self[i] != memory_dict[i]) or
            (i not in memory_dict and self[i] != positive_zero)
            for i in xrange(VMachine.MEMORY_SIZE)):
      return False
    else:
      return True

  def get_cur_word(self):
    return self[self.cur_addr]

  def clear_rI(self, reg):
    """Return True if overflowed"""
    if reg in "123456" and self.__dict__["r" + reg].word_list[1:4] != [0, 0, 0]:
      self.__dict__["r" + reg].word_list[1:4] = [0, 0, 0]
      return True
    else:
      return False

  def init_memory(self, memory):
    self.memory = [ Word() for _ in xrange(self.MEMORY_SIZE)]
    for addr, word in memory.items():
      # checking for correct input done in read_memory
      self[addr] = word

  def init_stuff(self):
    self.rA, self.rX, self.r0, self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.rJ =\
        [Word(0) for _ in xrange(10)]
    self.cf = 0
    self.of = False
    # self.devices = ... TODO

  def __init__(self, memory, start_address):
    self.errors = []
    self.init_memory(memory)
    self.init_stuff()
    self.cur_addr = start_address
    self.halted = False

  def print_state(self, file):
    file.write("HLT: %s\n" % self.halted)
    file.write("CA:  %s\n" % self.cur_addr)
    file.write("rA:  %s\n" % self.rA)
    file.write("rX:  %s\n" % self.rX)
    for i in xrange(1, 7):
      file.write("rI%i: %s\n" % (i, self.__dict__["r"+str(i)]))
    file.write("rJ:  %s\n" % self.rJ)
    file.write("CF:  ")
    assert(self.cf in (-1, 0, 1))
    if self.cf == -1:
      file.write("LESS")
    elif self.cf == 0:
      file.write("EQUAL")
    elif self.cf == 1:
      file.write("GREATER")
    file.write("\n")
    file.write("OF:  %s\n" % self.of)

  def step(self):
    try:
      execute(self)
    except VMError, e:
      self.errors.append( (self.cur_addr, e) )
