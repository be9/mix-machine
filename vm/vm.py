from vm_word import *
from vm_memory import *
from vm_command import cmdList
import vm_command_other
#import vm_command_jump
from vm_events import *

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
		
	# debug
	def __str__(self):
		regs = ""
		for i in self.regs:
			regs += "\t" + str(i) + ":\t" + str(self.regs[i]) + "\n"
		return "registers: \n" + str(regs) + "\nflags: \t\t" + str(self.flags) + "\ninstructions: \t" + str(self.instructions) + "\nhalted: \t" + str(self.is_halted) + "\n"

class VM:
	def __init__(self):
		self.context = VMContext()
		
	# debug
	def __str__(self):
		return str(context)
		
	def fill_memory(self, mem):
		pass
					
	def dump_memory(self, begin, end):
		pass
		
	
	def trace(self):
		print "--[trace]-----------------------------------------------"
		
		word = self.context.mem.get(self.context.regs["L"].addr())
		code = word.code()
		command = cmdList.get_command(code)
		
		try:		
			jmp = int(command.func(word, self.context))
			self.context.regs["L"].set_addr(jmp)
			self.context.instructions += command.time
		except VMHalt:
			self.context.is_halted = True
		
		print str(self.context)
		word = self.context.mem.get(self.context.regs["L"].addr())
		print str(word) + ":\t" + str(cmdList.get_command(word.code()))
		print "--------------------------------------------------------"
	
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
	
vm = VM()

vm.context.mem.set(Word([1,0,0,0,2,5]), 4)
for i in vm.context.mem.get_range(0, 10):
	print str(i)

vm.trace()
vm.trace()
vm.trace()
vm.trace()
vm.trace()
#vm.trace()
