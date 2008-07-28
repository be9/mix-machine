# add, sub, mul, div (c_codes = 1..4)

# ALL DONE

from word import *
from word_parser import *

def _add(vmachine, sign = 1):
  vmachine.cycles += 2

  addr = WordParser.get_full_addr(vmachine, False, True)
  left, right = WordParser.get_field_spec(vmachine)

  result = vmachine.rA[:] + sign * vmachine[addr][left:right]

  if abs(result) >= MAX_BYTE**10:
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

  addr = WordParser.get_full_addr(vmachine, False, True)
  left, right = WordParser.get_field_spec(vmachine)

  result = vmachine.rA[:] * vmachine[addr][left:right]
  sign = Word.sign(result)
  result = abs(result)

  vmachine.rA[1:5] = result / MAX_BYTE**5
  vmachine.rX[1:5] = result % MAX_BYTE**5
  vmachine.rA[0] = vmachine.rX[0] = sign


def div(vmachine):
  vmachine.cycles += 12

  addr = WordParser.get_full_addr(vmachine, False, True)
  left, right = WordParser.get_field_spec(vmachine)

  dividend = vmachine.rA[0] * (vmachine.rA[1:5] * MAX_BYTE**5 + vmachine.rX[1:5])
  divisor = vmachine[addr][left:right]
  if divisor == 0 or vmachine.rA[1:5] >= abs(divisor): # see Knuth book
    vmachine.of = True
    return

  vmachine.rX[0] = vmachine.rA[0]
  vmachine.rX[1:5] = dividend % divisor
  vmachine.rA[0:5] = dividend / divisor
