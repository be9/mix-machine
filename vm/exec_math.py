# add, sub, mul, div (c_codes = 1..4)

# ALL DONE

from word import *
from word_parser import *

def _add(vmachine, sign = 1):
  vmachine["cycles"] += 2

  addr = WordParser.get_full_addr(vmachine, check_mix_addr = True)
  left, right = WordParser.get_field_spec(vmachine)

  result = int(vmachine["A"]) + sign * int(vmachine[addr:left:right])

  if abs(result) >= MAX_BYTE**5:
    vmachine["of"] = True

  # "if result == 0 than we should save previous sign" - Knuth
  sign_word = vmachine["A":0:0]
  vmachine["A"] = result
  if result == 0:
    vmachine["A":0:0] = sign_word


def add(vmachine): _add(vmachine)
def sub(vmachine): _add(vmachine, -1)

def mul(vmachine):
  vmachine["cycles"] += 10

  addr = WordParser.get_full_addr(vmachine, check_mix_addr = True)
  left, right = WordParser.get_field_spec(vmachine)

  # multiply unsigned words
  result = int(vmachine["A":1:5]) * int(vmachine[addr:max(1, left):right])
  # signs of rA and rX from Knuth
  vmachine["A":0:0] = vmachine["X":0:0] = vmachine["A"][0] * vmachine[addr][0]

  vmachine["A":1:5] = result / MAX_BYTE**5
  vmachine["X":1:5] = result % MAX_BYTE**5


def div(vmachine):
  vmachine["cycles"] += 12

  addr = WordParser.get_full_addr(vmachine, check_mix_addr = True)
  left, right = WordParser.get_field_spec(vmachine)

  u_divisor = int(vmachine[addr:max(1, left):right])
  divisor_sign = vmachine[addr][0] if left == 0 else 1
  if u_divisor == 0 or int(vmachine["A":1:5]) >= u_divisor: # from Knuth book
    vmachine["of"] = True
    return
  u_dividend = int(vmachine["A":1:5]) * MAX_BYTE**5 + int(vmachine["X":1:5])

  vmachine["X":0:0] = vmachine["A":0:0] # sign of rX is previous sign of rA
  vmachine["A":0:0] = vmachine["A"][0] * divisor_sign # sign of rA - division sign
  vmachine["X":1:5] = u_dividend % u_divisor
  vmachine["A":1:5] = u_dividend / u_divisor
