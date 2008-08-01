from errors import *
from execution import *
from word_parser import *
from word import *

class VMachine:
  MEMORY_SIZE = 4000

  # constants for locking
  W_LOCKED = 0 # this cells are locked for write but you can read them
  RW_LOCKED = 1 # this cells are locked for read and write

  def __getitem__(self, index):
    """Can raise exception"""
    return self.memory[index]

  def __setitem__(self, index, word):
    """Can raise exception"""
    self.memory[index] = word

  @staticmethod
  def check_mem_addr(addr):
    return 0 <= addr < VMachine.MEMORY_SIZE

  def cmp_memory(self, memory_dict):
    """Need for testing"""
    positive_zero = [+1, 0, 0, 0, 0, 0]
    if not isinstance(memory_dict, dict) or \
       any( (i     in memory_dict and self[i].word_list != memory_dict[i].word_list) or
            (i not in memory_dict and self[i].word_list != positive_zero)
            for i in xrange(VMachine.MEMORY_SIZE)):
      return False
    else:
      return True

  def reg(self, r):
    return self.__dict__["r" + r]

  def set_reg(self, r, w):
    self.__dict__["r" + r] = Word(w)

  def get_cur_word(self):
    return self[self.cur_addr]

  def clear_rI(self, reg):
    """Return True if overflowed"""
    if reg in "123456" and self.__dict__["r" + reg].word_list[1:4] != [0, 0, 0]:
      self.__dict__["r" + reg].word_list[1:4] = [0, 0, 0]
      return True
    else:
      return False

  def set_memory(self, memory, reset):
    if reset:
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

  def set_device(self, number, device_instance):
    if 0 <= number < MAX_BYTE:
      self.devices[number] = device_instance
      return True
    else:
      return False

  def is_readable(self, addr):
    return addr not in self.locked_cells[self.RW_LOCKED]
  def is_writeable(self, addr):
    return addr not in ( self.locked_cells[self.W_LOCKED] | self.locked_cells[self.RW_LOCKED] )
  def is_readable_set(self, _set):
    return len(_set & self.locked_cells[self.RW_LOCKED]) == 0
  def is_writeable_set(self, _set):
    return len(_set & ( self.locked_cells[self.W_LOCKED] | self.locked_cells[self.RW_LOCKED] )) == 0

  def __init__(self, memory, start_address):
    self.errors = []
    self.set_memory(memory, reset = True)
    self.init_stuff()
    self.devices = {}
    self.locked_cells = [set(), set()]
    self.cur_addr = start_address
    self.halted = False
    self.cycles = 0

  def debug_state(self, file):
    try:
      file.write("CUR: %s\n" % self.get_cur_word())
    except:
      file.write("CUR: None\n")
    file.write("CYCLES: %s\n" % self.cycles)
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

  def debug_mem(self, file, begin, end):
    if begin > end:
      return
    for i in xrange(begin, end + 1):
      file.write("%04i %s\n" % (i, self[i]))

  def step(self):
    if not self.check_mem_addr(self.cur_addr):
      raise InvalidCurAddrError(self.cur_addr)
    cycles = execute(self)

    for dev in self.devices.values():
      unlock = dev.refresh(cycles)

      if unlock is not None:
        mode = self.W_LOCKED if unlock[0] == 'w' else self.RW_LOCKED
        self.locked_cells[mode] -= set(range(unlock[1][0], unlock[1][1] + 1))
