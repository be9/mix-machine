from vm_word import Word
from vm_command import cmdList
from vm_events import *

def nop(command, context):
	return context.regs["L"].addr() + 1

def spec(command, context):
	if command.fmt() == 0:
		return spec_num(command, context)
	elif command.fmt() == 1:
		return spec_char(command, context)
	elif command.fmt() == 2:
		return spec_hlt(command, context)
	else:
		return -1		# error: invalid fmt
		
def spec_num(command, context):
	return context.regs["L"].addr() + 1
def spec_char(command, context):
	return context.regs["L"].addr() + 1
def spec_hlt(command, context):
	raise VMHalt()
	return context.regs["L"].addr() + 1

	
cmdList.add_command(0, nop, 1, "NOP")
cmdList.add_command(5, spec, 10, "NUM, CHAR, HLT")