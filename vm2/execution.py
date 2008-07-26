
from errors import *
from exec_addr_manipulation import *
from exec_others import *
from exec_store import *
from exec_load import *

def find_nearest_down(array, value):
  # returns (result, Bool), where Bool - if result is exact (codes has value in keys)
  result = array[0]
  for x in array:
    if x < value:
      result = x
    elif x == value:
      return (value, True)
    else:
      break
  return (result, False)

def execute(vmachine):
  # some common stuff
  word = vmachine.get_cur_word()
  f = word[4]
  c = word[5]

  # list of sorted keys for search
  codes_sorted = codes.keys()
  codes_sorted.sort()
  # find instruction whith this codes
  nearest, exact = find_nearest_down(codes_sorted, (c, f))
  if codes[nearest][1] and not exact:
    raise UnknownInstructionError(tuple(word))
  codes[nearest][0](vmachine)




def _debug_fail():
  print "FAILED!!!!"
  raise "FAILED!!!!"

# boolean - is field-part fixed
codes = {
  (0, 0) : (nop, False),
  (5, 2) : (hlt, True),
  (15, 0) : (ldx, False),
  (24, 0) : (sta, False),
  (48, 2) : (enta, True),
  (49, 0) : (inc1, True),
  (55, 2) : (entx, True),
  (63, 63) : (_debug_fail, False)
}