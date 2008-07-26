from vm_word import *
from vm_memory import *
from vm_command import cmdList
from vm_events import *
from vm_errors import VMError, VMRuntimeError
from vm_context import VMContext
from vm_command_parser import ParsedCommand

#import vm_command_addr
import vm_command_cmp
#import vm_command_io
import vm_command_jump
import vm_command_load
#import vm_command_math
#import vm_command_store
import vm_command_other

class VM:
	"""The main interface for MIX machine"""
	def __init__(self):
		self.context = VMContext()
		self.cmd_list = cmdList
		
	def fill_memory(self, mem):
		pass
					
	def dump_memory(self, begin, end):
		pass
		
	
	def trace(self):
		word = self.context.mem.get(self.context.rL.int())
				
		parsed_cmd = ParsedCommand(word, self.context)
		
		code = parsed_cmd.w_code()
		fmt = parsed_cmd.w_fmt()
		
		command = self.cmd_list.get_command(code, fmt)
		
		try:
			command.func(parsed_cmd, self.context)
			
			if not command.is_jump:
				self.context.rL = Word(self.context.rL.int() + 1)
			self.context.instructions += command.time
			
		except VMRuntimeError, err:
			print "runtime error occured"
			print err
			
		except VMHalt:
			self.context.is_halted = True
	
	def run(self):
		pass
		
	def reset(self):
		pass
	
	# breakpoints
	def set_brakepoint(self):
		pass
	def remove_brakepoint(self):
		pass
	def remove_all_brakepoints(self):
		pass
	def get_all_breakpoints(self):
		pass