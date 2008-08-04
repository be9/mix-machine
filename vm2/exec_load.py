# ld* (c_code = 8..23)

# ALL DONE

from word_parser import *

def _ld(vmachine, reg, sign = 1):
  vmachine.cycles += 2

  # src - can be cell with address [-1, 0, 0] =(2dec)= 0
  src = vmachine[WordParser.get_full_addr(vmachine, check_mix_addr = True)]
  # dst - rREG
  left, right = WordParser.get_field_spec(vmachine)

  # result will be loaded to reg
  result = Word(src[max(1, left):right])
  result[0] = sign * (src[0] if left == 0 else +1)

  vmachine.set_reg(reg, result)
  if vmachine.clear_rI(reg):
    # overflow, but nothing do (see Knuth)
    pass

def lda(vmachine):  _ld(vmachine, "A")
def ld1(vmachine):  _ld(vmachine, "1")
def ld2(vmachine):  _ld(vmachine, "2")
def ld3(vmachine):  _ld(vmachine, "3")
def ld4(vmachine):  _ld(vmachine, "4")
def ld5(vmachine):  _ld(vmachine, "5")
def ld6(vmachine):  _ld(vmachine, "6")
def ldx(vmachine):  _ld(vmachine, "X")
def ldan(vmachine):  _ld(vmachine, "A", -1)
def ld1n(vmachine):  _ld(vmachine, "1", -1)
def ld2n(vmachine):  _ld(vmachine, "2", -1)
def ld3n(vmachine):  _ld(vmachine, "3", -1)
def ld4n(vmachine):  _ld(vmachine, "4", -1)
def ld5n(vmachine):  _ld(vmachine, "5", -1)
def ld6n(vmachine):  _ld(vmachine, "6", -1)
def ldxn(vmachine):  _ld(vmachine, "X", -1)
