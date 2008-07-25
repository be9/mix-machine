from vm_word import Word, CmdWord
from vm_context import VMContext

class CommandParser:
	def __init__(self):
		pass
	
	def parse_word(self, command, context):
		command = CmdWord(command)
		return { "w_addr" :	command.addr(),
			 "w_index" :	command.index(),
			 "w_fmt" :	command.fmt(),
			 "w_code" :	command.code(),
			 "M" :		command.addr() + context.get_reg_index(command.index()).int(),
			 "F" :		divmod(command.fmt(), 8)
			}