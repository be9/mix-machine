# s[l/r]* (c_codes = 6)

# ALL DONE

from errors import *
from word import *
from word_parser import *

LEFT  = 0
RIGHT = 1

def _s(vmachine, src, dir, cycle = False):
  assert(dir in (LEFT, RIGHT))
  length = len(src)
  shift = WordParser.get_full_addr(vmachine)
  if shift < 0:
    raise NegativeShiftError(shift)
  shift = shift % length if cycle else min(shift, length - 1)

  dst = [0] * length
  if dir == LEFT:
    dst[0 : length-shift] = src[shift : length]
    if cycle:
      dst[length-shift : length] = src[0 : shift]
  else:
    dst[shift : length] = src[0 : length-shift]
    if cycle:
      dst[0 : shift] = src[length-shift : length]
  return dst


def _sa(vmachine, dir):
  vmachine.rA.word_list[1:6] = _s(vmachine, vmachine.rA.word_list[1:6], dir)

def sla(vmachine):    _sa(vmachine, LEFT)
def sra(vmachine):    _sa(vmachine, RIGHT)


def _sax(vmachine, dir, cycle = False):
  res = _s(vmachine, vmachine.rA.word_list[1:6] + vmachine.rX.word_list[1:6], dir, cycle)
  vmachine.rA.word_list[1:6] = res[0:5]
  vmachine.rX.word_list[1:6] = res[5:10]

def slax(vmachine):   _sax(vmachine, LEFT)
def srax(vmachine):   _sax(vmachine, RIGHT)
def slc(vmachine):    _sax(vmachine, LEFT, True)
def src(vmachine):    _sax(vmachine, RIGHT, True)
