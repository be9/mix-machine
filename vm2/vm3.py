from virt_machine import *
from errors import *

error_dict = {
  InvalidMemAddrError     : 1,
  InvalidIndError         : 2,
  InvalidFieldSpecError   : 3,
  UnknownInstructionError : 4,
  InvalidCurAddrError     : 5,
  NegativeShiftError      : 6
}

class VM3:
  def __init__(self):
    self.vm = VMachine({}, 0)
    assert(len(self.vm.errors) == 0)

  def execute(self, at = None, start = None):
    assert( (at is not None) ^ (start is not None) )
    if at is not None:
      self.vm.cur_addr = at
      self.vm.step()
    else:
      self.vm.cur_addr = start
      while not self.vm.halted and len(self.vm.errors) == 0:
        self.vm.step()

  def load(self, mega):
    memory_part = dict( [(key, value) for key, value in mega.items() if isinstance(key, int)] )
    self.vm.set_memory(memory_part, reset = False)

    for reg in "AXJ":
      if mega.get(reg) is not None: self.vm.set_reg(reg, mega[reg])

    for reg in "123456":
      if mega.get("I"+reg) is not None: self.vm.set_reg(reg, mega["I"+reg])

    if mega.get("CA") is not None: self.vm.cur_addr = mega["CA"]
    if mega.get("CF") is not None: self.vm.cf = mega["CF"]
    if mega.get("OF") is not None: self.vm.of = bool(mega["OF"])

    assert(len(self.vm.errors) == 0)


  def state(self):
    """Returns MEGA hash"""
    mega = dict([ (i, self.vm[i]) for i in xrange(self.vm.MEMORY_SIZE) ])

    for reg in "AXJ":
      mega[reg] = self.vm.reg(reg)
    for reg in "123456":
      mega["I"+reg] = self.vm.reg(reg)

    mega["CA"] = self.vm.cur_addr
    mega["CF"] = self.vm.cf
    mega["OF"] = int(self.vm.of)

    if len(self.vm.errors) > 0: # can only be == 1
      mega["error"] = error_dict(type( self.vm.errors[0][1] ))
    else:
      mega["error"] = 0
    return mega
