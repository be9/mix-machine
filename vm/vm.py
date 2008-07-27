from vm_word import Word
from vm_memory import Memory, AddressOutOfRangeError
from vm_command import cmdList, CommandNotFoundError
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

class VMHaltedError(VMRuntimeError):
	pass

class VM:
	"""The main interface for MIX machine"""
	def __init__(self):
		self.context = VMContext()
		
	def trace(self):
		if self.context.is_halted:
			raise VMHaltedError()
		
		word = self.context.mem.get(self.context.rL.int())
				
		parsed_cmd = ParsedCommand(word, self.context)
		
		code = parsed_cmd.w_code()
		fmt = parsed_cmd.w_fmt()
		
		command = cmdList.get_command(code, fmt)
		
		try:
			command.func(parsed_cmd, self.context)
			
			if not command.is_jump:
				self.context.rL = Word(self.context.rL.int() + 1)
			self.context.instructions += command.time

		except VMHalt:
			self.context.is_halted = True
	
	def run(self):
		pass
