from virt_machine import *
from device import *
from vm2_errors import *
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm3'))
import vm3_errors

error_dict = {
  InvalidMemAddrError         : vm3_errors.InvalidAddress,
  InvalidIndError             : vm3_errors.InvalidIndex,
  InvalidFieldSpecError       : vm3_errors.InvalidFieldSpec,

  UnknownInstructionError     : vm3_errors.UnknownInstruction,
  InvalidCurAddrError         : vm3_errors.InvalidCA,

  MemReadLockedError          : vm3_errors.ReadLocked,
  MemWriteLockedError         : vm3_errors.WriteLocked,

  NegativeShiftError          : vm3_errors.NegativeShift,

  InvalidMoveError            : vm3_errors.InvalidMove,

  InvalidDeviceError          : vm3_errors.InvalidDevice,
  UnsupportedDeviceModeError  : vm3_errors.UnsupportedDeviceMode,
  InvalidCharError            : vm3_errors.InvalidChar,
  InvaliCharCodeError         : vm3_errors.InvalidCharCode,
  IOMemRangeError             : vm3_errors.IOMemRange
}

R_MODE = 'r'
W_MODE = 'w'
FILE_DEV = 0

class VM3:
  def __init__(self):
    self.vm = VMachine({}, 0)
    assert(len(self.vm.errors) == 0)

  def execute(self, at = None, start = None):
    """Returns number of cycles"""
    assert( (at is not None) ^ (start is not None) )
    try:
      self.vm.cycles = 0
      if at is not None:
        self.vm.cur_addr = at
        self.vm.step()
      else:
        self.vm.cur_addr = start
        while not self.vm.halted:
          self.vm.step()
      return self.vm.cycles
    except VMError, e:
      raise error_dict[type(e)]

  def hook(self, item, old, new):
    if self.hook_out is None:
      return
    real_new = new
    if item in "a x j".split():
      real_item = item.upper()
      real_new = new.word_list
    if item == "of":
      real_item = item.upper()
      real_new = int(new)
    elif item in "1 2 3 4 5 6".split():
      real_item = "I" + item
      real_new = new.word_list
    elif item == "halted":
      real_item = "HLT"
      real_new = int(new)
    elif item == "cur_addr":
      real_item = "CA"
    elif item == "cycles":
      return
    elif item == "cf":
      real_item = "CF"
    elif item == "w":
      real_item = "W_LOCKED"
    elif item == "rw":
      real_item = "RW_LOCKED"
    else:
      real_item = item
      real_new = new.word_list
    self.hook_out(real_item, None, real_new)

  def load(self, mega, devs = {}, hook = None):
    memory_part = {}

    for addr, word in mega.iteritems():
      if isinstance(addr, int):
        memory_part[addr] = Word(word)

    self.vm.set_memory(memory_part, reset = False)

    for reg in "AXJ":
      rv = mega.get(reg)
      if rv is not None: self.vm.set_reg(reg, Word(rv))

    for reg in "123456":
      rv = mega.get("I"+reg)
      if rv is not None: self.vm.set_reg(reg, Word(mega["I"+reg]))

    if mega.get("CA") is not None: self.vm.cur_addr = mega["CA"]
    if mega.get("CF") is not None: self.vm.cf = mega["CF"]
    if mega.get("OF") is not None: self.vm.of = bool(mega["OF"])
    if mega.get("HLT") is not None: self.vm.halted = bool(mega["HLT"])
    if mega.get("W_LOCKED")   is not None: self.vm.locked_cells[self.vm.W_LOCKED] =   set(mega["W_LOCKED"])
    if mega.get("RW_LOCKED")  is not None: self.vm.locked_cells[self.vm.RW_LOCKED] =  set(mega["RW_LOCKED"])
 
    self.vm.devices = {}
    for num, dev_info in devs.items():
      if dev_info[0] == FILE_DEV:
        # add device for working with file
        self.vm.set_device(num, FileDevice(dev_info[1], dev_info[2], dev_info[3], dev_info[4]))
      #elif dev_info[0] == ANOTHER_DEV:
        #self.vm.set_device(num, AnotherDevice(dev_info[1], dev_info[2], dev_info[3]))

    self.hook_out = hook
    self.vm.set_cpu_hook(self.hook)
    self.vm.set_mem_hook(self.hook)
    self.vm.set_lock_hook(self.hook)

    assert(len(self.vm.errors) == 0)

  def state(self):
    """Returns MEGA hash"""
    mega = dict([ (i, self.vm[i].word_list[:]) for i in xrange(self.vm.MEMORY_SIZE) ])

    for reg in "AXJ":
      mega[reg] = self.vm.reg(reg).word_list[:]
    for reg in "123456":
      mega["I"+reg] = self.vm.reg(reg).word_list[:]

    mega["CA"] = self.vm.cur_addr
    mega["CF"] = self.vm.cf
    mega["OF"] = int(self.vm.of)
    mega["HLT"] = int(self.vm.halted)
    mega["W_LOCKED"] =  self.vm.locked_cells[self.vm.W_LOCKED]
    mega["RW_LOCKED"] = self.vm.locked_cells[self.vm.RW_LOCKED]

    return mega
