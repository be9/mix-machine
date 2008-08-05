from vm2_errors import *
from word import *

class ParsedCommand:
	def __init__(self, word, vmachine):
		self.word = word
		self.vmachine = vmachine
		
	def w_addr(self):
		return self.word[0:2]
	
	def w_index(self):
		return self.word[3:3]
	
	def w_fmt(self):
		return self.word[4:4]
		
	def w_code(self):
		return self.word[5:5]
		
	def F(self):
		l, r = divmod(self.w_fmt(), 8)
		
		if l < 0 or l > r or r > 5:
			raise InvalidFieldSpecError("%i:%i=%i" % (l, r, self.w_fmt()))
		
		return l, r
	
	def I(self):
		idx = self.w_index()
		
		if not 0 <= idx <= 6:
			raise InvalidIndError(idx)
		
		return idx
	
	def M(self):
		idx = self.I()
		if idx != 0:
			return int( self.w_addr() + self.vmachine.reg(str(idx))[:] )
		else:
			return int( self.w_addr() )



class WordParser:
  @staticmethod
  def get_full_addr(vmachine, check_overflow = False, check_mix_addr = False):
    word = vmachine.get_cur_word()

    addr = ParsedCommand(word, vmachine).M()

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
    return ParsedCommand(word, vmachine).F()

  @staticmethod
  def get_sign(vmachine):
    return vmachine.get_cur_word()[0]

  @staticmethod
  def get_field(vmachine):
    return vmachine.get_cur_word()[4]
