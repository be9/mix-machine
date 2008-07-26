from vm_word import Word
from vm_memory import *
from vm_errors import VMError

class VMContextInvalidIndexError(VMError):
	def __init__(self, index):
		self = VMError("Invalid number of index register")
		self.index = index

class VMContext:
	def __init__(self):
		#self.regs = {	"A" :	Word(0),
		#		"X" : 	Word(0),
		#		"I1" :	Word(0),
		#		"I2" :	Word(0),
		#		"I3" :	Word(0),
		#		"I4" :	Word(0),
		#		"I5" :	Word(0),
		#		"J" : 	Word(0),
		#		"L" :	Word(0) }
				
		self.rA = Word(0)
		self.rX = Word(0)
		self.rI = (Word(0), Word(0), Word(0), Word(0), Word(0), Word(0), Word(0))	# must be different instances, rI[0] unused
		self.rJ = Word(0)
		self.rL = Word(0)
		
		#self.flags = {  "OF" : 0,
		#		"CF" : 0 }
				
		self.OF = 0
		self.CF = 0
	
		self.mem = Memory()
		self.mem.fill(0)
		
		self.instructions = 0
		
		self.is_halted = False
		
	def reset(self):
		self.rA = Word(0)
		self.rX = Word(0)
		self.rI = (Word(0), Word(0), Word(0), Word(0), Word(0), Word(0), Word(0))
		self.rJ = Word(0)
		self.rL = Word(0)
			
		self.OF = 0
		self.CF = 0
					
		self.mem.fill(0)
		
		self.instructions = 0
		self.is_halted = False
		
	# debug
	def __str__(self):
		regs = ""
		regs += "\t" + "rA" + ":\t" + str(self.rA) + "\n"
		regs += "\t" + "rX" + ":\t" + str(self.rX) + "\n"
		
		for i in xrange(1, 7):
			regs += "\t" + "rI"+str(i) + ":\t" + str(self.rI[i]) + "\n"
		
		regs += "\t" + "rJ" + ":\t" + str(self.rJ) + "\n"
		regs += "\t" + "rL" + ":\t" + str(self.rL) + "\n"
		
		flags = ""
		flags += "CF: " + str(self.CF) + ", "
		flags += "OF: " + str(self.OF)
		
		return "registers: \n" + str(regs) + "\nflags: \t\t" + str(flags) + "\ninstructions: \t" + str(self.instructions) + "\nhalted: \t" + str(self.is_halted) + "\n"

