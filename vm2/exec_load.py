# ld* (c_code = 8..23)

# ALL DONE

from word_parser import *

def _ld(vmachine, reg, sign = 1):
  src = vmachine[WordParser.get_full_addr(vmachine, False, True)]
  # dst - rREG
  left, right = WordParser.get_field_spec(vmachine)
  vmachine.__dict__["r" + reg] = Word(sign * src[left:right])
  if vmachine.clear_rI(reg):
    # overflow, but nothing do (see Knuth)
    pass

def lda(vmachine):
  _ld(vmachine, "A")

def ld1(vmachine):
  _ld(vmachine, "1")

def ld2(vmachine):
  _ld(vmachine, "2")

def ld3(vmachine):
  _ld(vmachine, "3")

def ld4(vmachine):
  _ld(vmachine, "4")

def ld5(vmachine):
  _ld(vmachine, "5")

def ld6(vmachine):
  _ld(vmachine, "6")

def ldx(vmachine):
  _ld(vmachine, "X")

def ldan(vmachine):
  _ld(vmachine, "A", -1)

def ld1n(vmachine):
  _ld(vmachine, "1", -1)

def ld2n(vmachine):
  _ld(vmachine, "2", -1)

def ld3n(vmachine):
  _ld(vmachine, "3", -1)

def ld4n(vmachine):
  _ld(vmachine, "4", -1)

def ld5n(vmachine):
  _ld(vmachine, "5", -1)

def ld6n(vmachine):
  _ld(vmachine, "6", -1)

def ldxn(vmachine):
  _ld(vmachine, "X", -1)
