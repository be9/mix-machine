# nop (c_code = 0), hlt, num, char (c_code = 5), move (c_code = 7)

# ALL DONE

from word import *
from word_parser import *

def nop(vmachine):
  vmachine.cycles += 1

def hlt(vmachine):
  vmachine.cycles += 10

  vmachine.halted = True
  vmachine.jump_to = vmachine.cur_addr

def num(vmachine):
  vmachine.cycles += 10

  # vmachine.rA.word_list[1:6] + vmachine.rX.word_list[1:6] - array of all bytes
  # reduce - create string of all digits
  # int - convert it to int
  # % MB**10 - to avoid overflow
  vmachine.rA[1:5] = int(reduce(lambda x, y : x+str(y % 10), vmachine.rA.word_list[1:6] + vmachine.rX.word_list[1:6], "")) % MAX_BYTE**10

def char(vmachine):
  vmachine.cycles += 10

  # vmachine.rA[1:5] - num for convert
  # str(num) - convert to string
  # map(lambda x : int(x) + 30, s) - get list of mix-chars
  seq = map(lambda x : int(x) + 30, str(vmachine.rA[1:5]))
  seq = [30] * (10 - len(seq)) + seq
  vmachine.rA.word_list[1:6] = seq[0:5]
  vmachine.rX.word_list[1:6] = seq[5:10]

def move(vmachine):
  # T = 1 + 2*F
  vmachine.cycles += 1

  num = WordParser.get_field(vmachine)
  if num == 0:
    return
  src = WordParser.get_full_addr(vmachine, check_mix_addr = True)
  dst = vmachine.r1[:]

  if not vmachine.is_readable_set(set(range(  src, src + num  ))):
    raise MemReadLockedError( (src, src + num - 1) )
  if not vmachine.is_writeable_set(set(range(  dst, dst + num  ))):
    raise MemReadLockedError( (dst, dst + num - 1) )

  if dst <0 or src < 0:
    raise InvalidMoveError( (num, src, dst) )
  # now all addresses would be greater than dst or src, so they are >= 0
  try:
    for i in xrange(num):
      vmachine[dst] = vmachine[src+i]
      dst += 1 # dst - like r1 always contains address of next destination word
      vmachine.cycles += 2
  except IndexError:
    vmachine.r1[:] = dst # it's not written in Knuth book, but it's very logically,
    raise InvalidMoveError( (num, src, vmachine.r1[:]) )
  else:
    vmachine.r1[:] = dst
