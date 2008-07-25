from vm_word import Word
from vm_command import cmdList
from vm_events import *

def nop(command, context):
	pass

def num(command, context):
	pass

def char(command, context):
	pass

def hlt(command, context):
	raise VMHalt()

	
cmdList.add_command(0,	-1, nop, 1,	"NOP")
cmdList.add_command(5,	 0, num, 10,	"NUM")
cmdList.add_command(5,	 1, char, 10,	"CHAR")
cmdList.add_command(5,	 2, hlt, 10,	"HLT")