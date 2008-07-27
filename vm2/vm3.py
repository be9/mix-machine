from virt_machine import *
from errors import *
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../vm3'))
import vm3_errors

error_dict = {
  InvalidMemAddrError     : vm3_errors.InvalidAddress,
  InvalidIndError         : vm3_errors.InvalidIndex,
  InvalidFieldSpecError   : vm3_errors.InvalidFieldSpec,
  UnknownInstructionError : vm3_errors.UnknownInstruction,
  InvalidCurAddrError     : vm3_errors.InvalidCA,
  NegativeShiftError      : vm3_errors.NegativeShift
}

class VM3:
  def __init__(self):
    self.vm = VMachine({}, 0)
    assert(len(self.vm.errors) == 0)

  def execute(self, at = None, start = None):
    assert( (at is not None) ^ (start is not None) )
    try:
      if at is not None:
        self.vm.cur_addr = at
        self.vm.step()
      else:
        self.vm.cur_addr = start
        while not self.vm.halted:
          self.vm.step()
    except VMError, e:
      raise error_dict[e]

  def load(self, mega):
    memory_part = dict( [(addr, Word(word)) for addr, word in mega.items() if isinstance(addr, int)] )
    self.vm.set_memory(memory_part, reset = False)

    for reg in "AXJ":
      if mega.get(reg) is not None: self.vm.set_reg(reg, Word(mega[reg]))

    for reg in "123456":
      if mega.get("I"+reg) is not None: self.vm.set_reg(reg, Word(mega["I"+reg]))

    if mega.get("CA") is not None: self.vm.cur_addr = mega["CA"]
    if mega.get("CF") is not None: self.vm.cf = mega["CF"]
    if mega.get("OF") is not None: self.vm.of = bool(mega["OF"])
    if mega.get("HLT") is not None: self.vm.halted = bool(mega["HLT"])

    assert(len(self.vm.errors) == 0)


  def state(self):
    """Returns MEGA hash"""
    mega = dict([ (i, self.vm[i].word_list) for i in xrange(self.vm.MEMORY_SIZE) ])

    for reg in "AXJ":
      mega[reg] = self.vm.reg(reg).word_list
    for reg in "123456":
      mega["I"+reg] = self.vm.reg(reg).word_list

    mega["CA"] = self.vm.cur_addr
    mega["CF"] = self.vm.cf
    mega["OF"] = int(self.vm.of)
    mega["HLT"] = int(self.vm.halted)

    return mega
