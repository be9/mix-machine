# nop (c_code = 0), hlt, num, char (c_code = 5)

# ALL DONE

from word import *

def nop(vmachine):
  vmachine.cycles += 1

def hlt(vmachine):
  vmachine.cycles += 10

  vmachine.halted = True

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
  seq = [30] * min(0, 10-len(seq)) + seq
  vmachine.rA.word_list[1:6] = seq[0:5]
  vmachine.rX.word_list[1:6] = seq[5:10]
