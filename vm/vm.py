from vm_word import Word
from vm_memory import Memory, AddressOutOfRangeError
from vm_command import cmdList, CommandNotFonudError
from vm_events import VMEvent, VMStop, VMHalt
from vm_errors import VMError, VMRuntimeError
from vm_context import VMContext
from vm_command_parser import ParsedCommand, CommandInvalidIndexError, CommandInvalidFormatError

#import vm_command_addr
import vm_command_cmp
#import vm_command_io
import vm_command_jump
import vm_command_load
#import vm_command_math
#import vm_command_store
import vm_command_other

class VMHaledError(VMRuntimeError):
	pass

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
		if self.context.is_halted:
			raise VMHaledError()
		
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