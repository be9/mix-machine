# st*
from word_parser import *

def _st(vmachine, reg):
  src = vmachine.__dict__["r" + reg]
  # dst - vmachine[addr]
  addr = WordParser.get_full_addr(vmachine, True)
  left, right = WordParser.get_field_spec(vmachine)
  vmachine[addr][left:right] = src[:]
  vmachine.cur_addr += 1

def sta(vmachine):
  _st(vmachine, "A")
