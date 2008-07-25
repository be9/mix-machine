from vm_word import *
from vm_memory import *
from vm_command import cmdList
from vm_events import *
from vm_errors import VMError
from vm_context import VMContext

#import vm_command_addr
import vm_command_cmp
#import vm_command_io
import vm_command_jump
import vm_command_load
#import vm_command_math
import vm_command_store
import vm_command_other

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
		word = CmdWord(self.context.mem.get(self.context.regs["L"].int()))
		code = word.code()
		fmt = word.fmt()
		command = cmdList.get_command(code, fmt)
		
		try:
			jmp = int(command.func(word, self.context))
			self.context.regs["L"] = Word(jmp)
			self.context.instructions += command.time
		except VMHalt:
			self.context.is_halted = True
	
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