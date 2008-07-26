from errors import *
from word import *

class WordParser:
  @staticmethod
  def get_full_addr(vmachine, check_mix_addr = False):
    word = vmachine.get_cur_word()
    addr = word[0:2]
    ind = word[3]
    if ind > 6:
      raise InvalidIndError(ind)
    addr += vmachine.__dict__["r"+str(ind)][:]
    if abs(addr) >= MAX_BYTE**2:
      #FIX ME - overflow
      addr = Word.sign(addr) * ( abs(addr) % MAX_BYTE**2  )
    if check_mix_addr and not vmachine.check_mem_addr(addr):
      raise InvalidMemAddrError(addr)
    return addr

  @staticmethod
  def get_field_spec(vmachine):
    word = vmachine.get_cur_word()
    l = word[4] / 8
    r = word[4] % 8
    if not (0 <= l <= r <= 6):
      raise InvalidFieldSpecError("%i:%i=%i" % l, r, word[4])
    return (l, r)