from exec_addr_manipulation import *
from exec_others import *
from errors import *


def _debug_fail():
  print "FAILED!!!!"
  raise "FAILED!!!!"

# boolean - is field-part fixed
codes = {
  0 : (nop, False),
  322 : (hlt, True),
  3074 : (enta, True),
  3522 : (entx, True),
  4000 : (_debug_fail, False)
}

def find_nearest_down(array, value):
  # returns (result, Bool), where Bool - if result is exact (codes has value in keys)
  result = array[0]
  for x in array[1:]:
    if x < value:
      result = x
    elif x == value:
      return (value, True)
    else:
      break
  return (result, False)

def execute(vmachine):
  # some common stuff
  word = vmachine[vmachine.cur_addr]
  addr = word[0] * (word[1] * vmachine.MAX_BYTE + word[2])
  ind = word[3]
  f = word[4]
  c = word[5]

  # list of sorted keys for search
  codes_sorted = codes.keys()
  codes_sorted.sort()

  # find instruction whith this codes
  nearest, exact = find_nearest_down(codes_sorted, c * vmachine.MAX_BYTE + f)
  if codes[nearest][1] and not exact:
    raise UnknownInstructionError(tuple(word))
  codes[nearest][0](vmachine, addr, ind, f, c)
