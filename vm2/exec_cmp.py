# cmp* (c_code = 56..63)

# ALL DONE
from word_parser import *

def _cmp(vmachine, reg):
  vmachine.cycles += 2

  addr = WordParser.get_full_addr(vmachine, check_mix_addr = True)
  if not vmachine.is_readable(addr):
    raise MemReadLockedError( (addr, addr) )
  left, right = WordParser.get_field_spec(vmachine)

  vmachine["cf"] = cmp(int(vmachine[reg:left:right]), int(vmachine[addr:left:right]))

def cmpa(vmachine):  _cmp(vmachine, "A")
def cmp1(vmachine):  _cmp(vmachine, "1")
def cmp2(vmachine):  _cmp(vmachine, "2")
def cmp3(vmachine):  _cmp(vmachine, "3")
def cmp4(vmachine):  _cmp(vmachine, "4")
def cmp5(vmachine):  _cmp(vmachine, "5")
def cmp6(vmachine):  _cmp(vmachine, "6")
def cmpx(vmachine):  _cmp(vmachine, "X")
