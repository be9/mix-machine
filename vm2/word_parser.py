from errors import *

class WordParser:
  def __init__(self, vmachine):
    self.vmachine = vmachine

  def get_full_addr(self):
    word = self.vmachine.get_cur_word()
    addr = word[0] * ( word[1] * self.vmachine.MAX_BYTE + word[2] )
    ind = word[3]
    if ind > 6:
      raise InvalidIndError(ind)
    addr += self.vmachine.mix2dec(self.vmachine.rI[ind])
    addr = self.vmachine.sign(addr) * ( abs(addr) % self.vmachine.MAX_BYTE**2 )
    return addr
