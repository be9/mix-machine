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
		
		self.instructions = 0	# how to name instruction counter?
		
	def reset(self):
		for i in self.regs:
			self.regs[i] = Word(0)
			
		for i in self.flags:
			self.flags[i] = 0
			
		self.mem.fill(0)
		
		self.instructions = 0
		
	# debug
	def __str__(self):
		regs = ""
		for i in self.regs:
			regs += "\t" + str(i) + ":\t" + str(self.regs[i]) + "\n"
		return "registers: \n" + str(regs) + "flags: \n\t" + str(self.flags) + "\ninstructions: \n\t" + str(self.instructions) + "\n"

class VM:
	def __init__(self):
		self.context = WMContext()
		
	# debug
	def __str__(self):
		return str(context)
		
	def fill_memory(self, mem):
		pass
					
	def dump_memory(self, begin, end):
		pass
		
	
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