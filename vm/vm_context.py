from vm_word import Word
from vm_memory import *
from vm_errors import VMError

class VMContextInvalidIndexError(VMError):
	def __init__(self, index):
		self = VMError("Invalid number of index register")
		self.index = index

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
		
		self.instructions = 0
		
		self.is_halted = False
		
	def reset(self):
		for i in self.regs:
			self.regs[i] = Word(0)
			
		for i in self.flags:
			self.flags[i] = 0
			
		self.mem.fill(0)
		
		self.instructions = 0
		self.is_halted = False
		
	def get_reg_index(self, index):
		if index == 0:
			return Word(0)
		elif index > 0 and index < 7:
			return Word(self.regs["I" + str(index)])
		else:
			raise VMContextInvalidIndexError(index)
		
	def set_reg_index(self, index, value):
		if index > 0 and index < 7:
			self.regs["I" + str(index)] = Word(value)
			return Word(self.regs["I" + str(index)])
		else:
			raise VMContextInvalidIndexError(index)
		
	def get_reg_l(self):
		return self.regs["L"]
	
	def set_reg_l(self, value):
		self.regs["L"] = value
		
	# debug
	def __str__(self):
		regs = ""
		for i in self.regs:
			regs += "\t" + str(i) + ":\t" + str(self.regs[i]) + "\n"
		return "registers: \n" + str(regs) + "\nflags: \t\t" + str(self.flags) + "\ninstructions: \t" + str(self.instructions) + "\nhalted: \t" + str(self.is_halted) + "\n"

