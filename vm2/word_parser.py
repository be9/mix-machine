from errors import *
from word import *

class WordParser:
  @staticmethod
  def get_full_addr(vmachine, check_overflow = False, check_mix_addr = False):
    word = vmachine.get_cur_word()
    addr = word[0:2]
    ind = word[3]
    if ind > 6:
      raise InvalidIndError(ind)
    addr += vmachine.reg(str(ind))[:]
    if abs(addr) >= MAX_BYTE**2:
      addr = Word.norm_2bytes(addr)
      if check_overflow:
        vmachine.of = True
    if check_mix_addr and not vmachine.check_mem_addr(addr):
      raise InvalidMemAddrError(addr)
    return addr

  @staticmethod
  def get_field_spec(vmachine):
    word = vmachine.get_cur_word()
    l = word[4] / 8
    r = word[4] % 8
    if not (0 <= l <= r <= 5):
      raise InvalidFieldSpecError("%i:%i=%i" % (l, r, word[4]))
    return (l, r)

  @staticmethod
  def get_sign(vmachine):
    return vmachine.get_cur_word()[0]

  @staticmethod
  def get_field(vmachine):
    return vmachine.get_cur_word()[4]