from vm2_errors import *
from execution import *
from word_parser import *
from word import *

TRIGGERS = "cf of cur_addr halted cycles".split()

class VMachine:
  MEMORY_SIZE = 4000

  # constants for locking
  W_LOCKED = 0 # this cells are locked for write but you can read them
  RW_LOCKED = 1 # this cells are locked for read and write

  def __getitem__(self, x):
    """Can raise exception"""
    if x in TRIGGERS:
      return self.__dict__[x]
    if isinstance(x, slice): # slice, vm[2000:2:4] = ...
      item = x.start
      left = x.stop if x.stop is not None else 0
      right = x.step if x.step is not None else 5
    else: # vm[2000] = ...
      item = x
      left = 0
      right = 5
    return (self.memory[item] if isinstance(item, int) else self.reg(item))[left:right]

  def __setitem__(self, x, value):
    """Can raise exception"""
    if isinstance(x, slice): # slice, vm[2000:2:4] = ...
      item = x.start
      left = x.stop if x.stop is not None else 0
      right = x.step if x.step is not None else 5
    else: # vm[2000] = ...
      item = x
      left = 0
      right = 5
    old_value = self[item]
    if isinstance(item, int):
      # we are working with memory
      self.memory[item][left:right] = value
      if self.mem_hook is not None and old_value != self.memory[item]:
        self.mem_hook(item, old_value, self.memory[item])
    else:
      # we are working with registers or triggers
      if item in TRIGGERS:
        self.__dict__[item] = value
      else: # register
        self.reg(item)[left:right] = value
      if self.cpu_hook is not None and old_value != self[item]:
        self.cpu_hook(item, old_value, self[item])

  def reg(self, r):
    return self.__dict__["r" + r]
  def set_reg(self, r, w):
    self.__dict__["r" + r] = Word(w)


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
    if isinstance(memory, list):
      self.memory = [ Word(x) for x in memory]
      return
    if reset:
      self.memory = [ Word() for _ in xrange(self.MEMORY_SIZE)]
    for addr, word in memory.items():
      # checking for correct input done in read_memory
      self[addr] = word

  def init_stuff(self, start_address):
    self.rA, self.rX, self.r0, self.r1, self.r2, self.r3, self.r4, self.r5, self.r6, self.rJ =\
        [Word(0) for _ in xrange(10)]
    self.cf = 0
    self.of = False
    self.cur_addr = start_address
    self.halted = False

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

  def lock_cells(self, mode, add = None, sub = None):
    assert( (add is not None) ^ (sub is not None) )
    if self.lock_hook is not None:
      old = set(self.locked_cells[mode])
    if add is not None:
      # add set to self.locked_cells[mode]
      self.locked_cells[mode] |= add
    else:
      # subtract set from self.locked_cells[mode]
      self.locked_cells[mode] -= sub
    if self.lock_hook is not None and self.locked_cells[mode] != old:
      self.lock_hook(mode, old, self.locked_cells[mode])

  def __init__(self, memory, start_address):
    self.errors = []
    self.set_cpu_hook(None)
    self.set_mem_hook(None)
    self.set_lock_hook(None)
    self.set_memory(memory, reset = True)
    self.init_stuff(start_address)
    self.devices = {}
    self.locked_cells = [set(), set()]
    self.cycles = 0

  def step(self):
    if not self.check_mem_addr(self.cur_addr):
      raise InvalidCurAddrError(self.cur_addr)
    cycles = execute(self)

    # refresh all plugged devices
    for dev in self.devices.values():
      # if device isn't busy returns None
      unlock = dev.refresh(cycles)
      if unlock is not None:
        # else returned (mode, limits) - mode in 'rw', limits = (left, right) - properies of unlocked memory part
        if unlock[0] == 'w':
          mode = self.W_LOCKED
        elif unlock[0] == 'rw':
          mode = self.RW_LOCKED
        else:
          return # ioc busy
        # unlock memory
        self.lock_cells(mode, sub = set(range(unlock[1][0], unlock[1][1] + 1)))

  def set_cpu_hook(self, hook):
    self.cpu_hook = hook

  def set_mem_hook(self, hook):
    self.mem_hook = hook

  def set_lock_hook(self, hook):
    self.lock_hook = hook
