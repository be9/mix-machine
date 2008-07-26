# ld*
from word_parser import *

def _ld(vmachine, reg):
  src = vmachine[WordParser.get_full_addr(vmachine, True)]
  # dst - rREG
  left, right = WordParser.get_field_spec(vmachine)
  vmachine.__dict__["r" + reg] = Word(src[left:right])
  vmachine.cur_addr += 1

def ldx(vmachine):
  _ld(vmachine, "X")
