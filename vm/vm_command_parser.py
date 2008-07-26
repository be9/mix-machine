from vm_word import Word
from vm_context import VMContext
from vm_errors import VMError

class CommandIllegalIndex(VMError):
	pass

class CommandIllegalFormat(VMError):
	pass
	

class ParsedCommand:
	def __init__(self, word, context):
		self.word = word
		self.context = context
		
	def w_addr(self):
		return self.word.int((0,2))
	
	def w_index(self):
		return self.word.int((3,3))
	
	def w_fmt(self):
		return self.word.int((4,4))
		
	def w_code(self):
		return self.word.int((5,5))
		
	def F(self):
		F = divmod(self.w_fmt(), 8)
		
		if F[0] < 0 or F[0] > F[1] or F[1] > 5:
			raise "illegal fmt for command"
		
		return F
	
	def I(self):
		I = self.w_index()
		
		if  I < 0 or I > 6:
			raise "illegal index for command"
		
		return I
	
	def M(self):
		if self.I() != 0:
			return self.w_addr() + self.context.rI[self.I()]
		else:
			return self.w_addr()