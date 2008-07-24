from vm_word import Word
from vm_command import cmdList
from vm_events import *

def nop(command, context):
	return context.regs["L"].addr() + 1

def num(command, context):
	return context.regs["L"].addr() + 1

def char(command, context):
	return context.regs["L"].addr() + 1

def hlt(command, context):
	raise VMHalt()
	return context.regs["L"].addr() + 1

	
cmdList.add_command(0,	-1, nop, 1,	"NOP")
cmdList.add_command(5,	 0, num, 10,	"NUM")
cmdList.add_command(5,	 1, char, 10,	"CHAR")
cmdList.add_command(5,	 2, hlt, 10,	"HLT")