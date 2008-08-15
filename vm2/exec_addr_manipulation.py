# inc, dec, ent, enn (c_code = 48..55)

# ALL DONE

from word_parser import *

def _linear_manipulation(vmachine, reg, sign, inc_action):
  vmachine.cycles += 1

  """Inc-Action is 1 or 0"""
  result = inc_action * int(vmachine[reg]) + sign * WordParser.get_full_addr(vmachine, check_overflow = True)
  if result == 0:
    if inc_action:
      # if inc/dec sign is from previous register (line in ADD)
      w_result = Word( [vmachine[reg:0:0][0], 0, 0, 0, 0, 0] )
    else:
      # if ent/enn sign is from M (line in LD*)
      w_result = Word( [sign * WordParser.get_sign(vmachine), 0, 0, 0, 0, 0] )
  else:
    if abs(result) >= MAX_BYTE**2:
      result = Word.norm_2bytes(result)
      vmachine.of = True
    w_result = Word(result)
  vmachine[reg] = w_result

#----------------ENT/ENN--------------------
def _ent(vmachine, reg, sign = 1):
  _linear_manipulation(vmachine, reg, sign, 0)

def enta(vmachine):  _ent(vmachine, "A")
def ent1(vmachine):  _ent(vmachine, "1")
def ent2(vmachine):  _ent(vmachine, "2")
def ent3(vmachine):  _ent(vmachine, "3")
def ent4(vmachine):  _ent(vmachine, "4")
def ent5(vmachine):  _ent(vmachine, "5")
def ent6(vmachine):  _ent(vmachine, "6")
def entx(vmachine):  _ent(vmachine, "X")
def enna(vmachine):  _ent(vmachine, "A", -1)
def enn1(vmachine):  _ent(vmachine, "1", -1)
def enn2(vmachine):  _ent(vmachine, "2", -1)
def enn3(vmachine):  _ent(vmachine, "3", -1)
def enn4(vmachine):  _ent(vmachine, "4", -1)
def enn5(vmachine):  _ent(vmachine, "5", -1)
def enn6(vmachine):  _ent(vmachine, "6", -1)
def ennx(vmachine):  _ent(vmachine, "X", -1)

#----------------INC/DEC--------------------
def _inc(vmachine, reg, sign = 1):
  _linear_manipulation(vmachine, reg, sign, 1)

def inca(vmachine):  _inc(vmachine, "A")
def inc1(vmachine):  _inc(vmachine, "1")
def inc2(vmachine):  _inc(vmachine, "2")
def inc3(vmachine):  _inc(vmachine, "3")
def inc4(vmachine):  _inc(vmachine, "4")
def inc5(vmachine):  _inc(vmachine, "5")
def inc6(vmachine):  _inc(vmachine, "6")
def incx(vmachine):  _inc(vmachine, "X")
def deca(vmachine):  _inc(vmachine, "A", -1)
def dec1(vmachine):  _inc(vmachine, "1", -1)
def dec2(vmachine):  _inc(vmachine, "2", -1)
def dec3(vmachine):  _inc(vmachine, "3", -1)
def dec4(vmachine):  _inc(vmachine, "4", -1)
def dec5(vmachine):  _inc(vmachine, "5", -1)
def dec6(vmachine):  _inc(vmachine, "6", -1)
def decx(vmachine):  _inc(vmachine, "X", -1)
