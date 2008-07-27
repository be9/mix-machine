
from errors import *

from exec_addr_manipulation import *    # ALL DONE
from exec_cmp import *                  # ALL DONE
from exec_load import *                 # ALL DONE
from exec_others import *               # NOP, HLT, NUM, CHAR
from exec_store import *                # ALL DONE
from exec_math import *                 # ALL DONE
from exec_shift import *                # ALL DONE

def execute(vmachine):
  # some common stuff
  word = vmachine.get_cur_word()
  f = word[4]
  c = word[5]

  proc = codes.get(c, codes.get((c,f), None))

  if proc is not None:
    proc(vmachine)
  else:
    raise UnknownInstructionError(tuple(word))

def _debug_fail():
  print "FAILED!!!!"
  raise "FAILED!!!!"

# boolean - is field-part fixed
codes = {
  ( 0   ) : nop,
  ( 1   ) : add,
  ( 2   ) : sub,
  ( 3   ) : mul,
  ( 4   ) : div,
  ( 5, 0) : num,
  ( 5, 1) : char,
  ( 5, 2) : hlt,
  ( 6, 0) : sla,
  ( 6, 1) : sra,
  ( 6, 2) : slax,
  ( 6, 3) : srax,
  ( 6, 4) : slc,
  ( 6, 5) : src,
  ( 8   ) : lda,
  ( 9   ) : ld1,
  (10   ) : ld2,
  (11   ) : ld3,
  (12   ) : ld4,
  (13   ) : ld5,
  (14   ) : ld6,
  (15   ) : ldx,
  (16   ) : ldan,
  (17   ) : ld1n,
  (18   ) : ld2n,
  (19   ) : ld3n,
  (20   ) : ld4n,
  (21   ) : ld5n,
  (22   ) : ld6n,
  (23   ) : ldxn,
  (24   ) : sta,
  (25   ) : st1,
  (26   ) : st2,
  (27   ) : st3,
  (28   ) : st4,
  (29   ) : st5,
  (30   ) : st6,
  (31   ) : stx,
  (32   ) : stj,
  (33   ) : stz,
  (48, 0) : inca,
  (48, 1) : deca,
  (48, 2) : enta,
  (48, 3) : enna,
  (49, 0) : inc1,
  (49, 1) : dec1,
  (49, 2) : ent1,
  (49, 3) : enn1,
  (50, 0) : inc2,
  (50, 1) : dec2,
  (50, 2) : ent2,
  (50, 3) : enn2,
  (51, 0) : inc3,
  (51, 1) : dec3,
  (51, 2) : ent3,
  (51, 3) : enn3,
  (52, 0) : inc4,
  (52, 1) : dec4,
  (52, 2) : ent4,
  (52, 3) : enn4,
  (53, 0) : inc5,
  (53, 1) : dec5,
  (53, 2) : ent5,
  (53, 3) : enn5,
  (54, 0) : inc6,
  (54, 1) : dec6,
  (54, 2) : ent6,
  (54, 3) : enn6,
  (55, 0) : incx,
  (55, 1) : decx,
  (55, 2) : entx,
  (55, 3) : ennx,
  (56   ) : cmpa,
  (57   ) : cmp1,
  (58   ) : cmp2,
  (59   ) : cmp3,
  (60   ) : cmp4,
  (61   ) : cmp5,
  (62   ) : cmp6,
  (63   ) : cmpx,
}
