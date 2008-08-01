# add, sub, mul, div (c_codes = 1..4)

# ALL DONE

from word import *
from word_parser import *

def _add(vmachine, sign = 1):
  vmachine.cycles += 2

  addr = WordParser.get_full_addr(vmachine, check_mix_addr = True)
  left, right = WordParser.get_field_spec(vmachine)

  result = vmachine.rA[:] + sign * vmachine[addr][left:right]

  if abs(result) >= MAX_BYTE**5:
    vmachine.of = True

  # "if result == 0 than we should save previous sign" - Knuth
  sign = vmachine.rA[0]
  vmachine.rA = Word(result)
  if result == 0:
    vmachine.rA[0] = sign



def add(vmachine): _add(vmachine)
def sub(vmachine): _add(vmachine, -1)

def mul(vmachine):
  vmachine.cycles += 10

  addr = WordParser.get_full_addr(vmachine, check_mix_addr = True)
  left, right = WordParser.get_field_spec(vmachine)

  # multiply unsigned words
  result = vmachine.rA[1:5] * vmachine[addr][max(1, left):right]
  # signs of rA and rX from Knuth
  vmachine.rA[0] = vmachine.rX[0] = vmachine.rA[0] * vmachine[addr][0]

  vmachine.rA[1:5] = result / MAX_BYTE**5
  vmachine.rX[1:5] = result % MAX_BYTE**5


def div(vmachine):
  vmachine.cycles += 12

  addr = WordParser.get_full_addr(vmachine, check_mix_addr = True)
  left, right = WordParser.get_field_spec(vmachine)

  u_divisor = vmachine[addr][max(1, left):right]
  divisor_sign = vmachine[addr][0] if left == 0 else 1
  if u_divisor == 0 or vmachine.rA[1:5] >= u_divisor: # from Knuth book
    vmachine.of = True
    return
  u_dividend = vmachine.rA[1:5] * MAX_BYTE**5 + vmachine.rX[1:5]

  vmachine.rX[0] = vmachine.rA[0] # sign of rX is previous sign of rA
  vmachine.rA[0] = vmachine.rA[0] * divisor_sign # sign of rA - division sign
  vmachine.rX[1:5] = u_dividend % u_divisor
  vmachine.rA[1:5] = u_dividend / u_divisor
