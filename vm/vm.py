from vm_word import *
from vm_memory import *

class VMContext:
	def __init__(self):
		self.regs = {	"A" :	Word(0),
							"X" : 	Word(0),
							"I1" :	Word(0),
							"I2" :	Word(0),
							"I3" :	Word(0),
							"I4" :	Word(0),
							"I5" :	Word(0),
							"I6" :	Word(0),
							"J" : 	Word(0),
							"L" :	Word(0) }
							
		self.flags = {  "OF" : 0,
							"CF" : 0 }
							
		self.mem = Memory()
		self.mem.fill(0)
		
		self.count = 0	# how to name instruction counter?

class VM:
	def __init__(self):
		self.context = WMContext()
		
	# debug
	def __str__(self):
		return str(self.regs) + "\n"+  str(self.flags)
		
	def fill_memory(self, mem):
		for i in xrange(0, MEM_SIZE) :
			self.mem[i] = Word(mem[i])
			
	def dump_memory(self, begin, end):
		return [self.mem[i] for i in xrange(begin, end, 1)]
	
	def trace(self):
		pass
	
	def run(self):
		pass
		
	def reset(self):
		pass
	
	def set_brakepoint(self):
		pass
	def remove_brakepoint(self):
		pass
	def remove_all_brakepoints(self):
		pass
	def get_all_breakpoints(self):
		pass

pass
#mem = [Word(0)]*MEM_SIZE

#mem[0] = Word([1,2,3,4,5])
#mem[1] = Word([2,2,3,4,5])

#vm = VM()
#vm.fill_memory(mem)

#print [str(i) for i in vm.dump_memory(0, MEM_SIZE) ]
