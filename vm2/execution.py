
from errors import *

from exec_addr_manipulation import *    # ALL DONE
from exec_cmp import *                  # ALL DONE
from exec_load import *                 # ALL DONE
from exec_others import *               # NOP and HLT
from exec_store import *                # ALL DONE

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
  ( 8, 0) : (lda, False),
  ( 9, 0) : (ld1, False),
  (10, 0) : (ld2, False),
  (11, 0) : (ld3, False),
  (12, 0) : (ld4, False),
  (13, 0) : (ld5, False),
  (14, 0) : (ld6, False),
  (15, 0) : (ldx, False),
  (16, 0) : (ldan, False),
  (17, 0) : (ld1n, False),
  (18, 0) : (ld2n, False),
  (19, 0) : (ld3n, False),
  (20, 0) : (ld4n, False),
  (21, 0) : (ld5n, False),
  (22, 0) : (ld6n, False),
  (23, 0) : (ldxn, False),
  (24, 0) : (sta, False),
  (25, 0) : (st1, False),
  (26, 0) : (st2, False),
  (27, 0) : (st3, False),
  (28, 0) : (st4, False),
  (29, 0) : (st5, False),
  (30, 0) : (st6, False),
  (31, 0) : (stx, False),
  (32, 0) : (stj, False),
  (33, 0) : (stz, False),
  (48, 0) : (inca, True),
  (48, 1) : (deca, True),
  (48, 2) : (enta, True),
  (48, 3) : (enna, True),
  (49, 0) : (inc1, True),
  (49, 1) : (dec1, True),
  (49, 2) : (ent1, True),
  (49, 3) : (enn1, True),
  (50, 0) : (inc2, True),
  (50, 1) : (dec2, True),
  (50, 2) : (ent2, True),
  (50, 3) : (enn2, True),
  (51, 0) : (inc3, True),
  (51, 1) : (dec3, True),
  (51, 2) : (ent3, True),
  (51, 3) : (enn3, True),
  (52, 0) : (inc4, True),
  (52, 1) : (dec4, True),
  (52, 2) : (ent4, True),
  (52, 3) : (enn4, True),
  (53, 0) : (inc5, True),
  (53, 1) : (dec5, True),
  (53, 2) : (ent5, True),
  (53, 3) : (enn5, True),
  (54, 0) : (inc6, True),
  (54, 1) : (dec6, True),
  (54, 2) : (ent6, True),
  (54, 3) : (enn6, True),
  (55, 0) : (incx, True),
  (55, 1) : (decx, True),
  (55, 2) : (entx, True),
  (55, 3) : (ennx, True),
  (56, 0) : (cmpa, False),
  (57, 0) : (cmp1, False),
  (58, 0) : (cmp2, False),
  (59, 0) : (cmp3, False),
  (60, 0) : (cmp4, False),
  (61, 0) : (cmp5, False),
  (62, 0) : (cmp6, False),
  (63, 0) : (cmpx, False),
}