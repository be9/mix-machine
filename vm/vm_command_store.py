from vm_word import Word
from vm_command import cmdList

def sta(command, context):
	pass

def stx(command, context):
	pass

def sti(command, context):
	pass

def stj(command, context):
	pass

def stz(command, context):
	pass

cmdList.add_command(24,	-1, sta, 1,	"STA")
cmdList.add_command(31,	-1, stx, 1,	"STX")

cmdList.add_command(25,	-1, sti, 1,	"STI1")
cmdList.add_command(26,	-1, sti, 1,	"STI2")
cmdList.add_command(27,	-1, sti, 1,	"STI3")
cmdList.add_command(28,	-1, sti, 1,	"STI4")
cmdList.add_command(29,	-1, sti, 1,	"STI5")
cmdList.add_command(30,	-1, sti, 1,	"STI6")

cmdList.add_command(32,	-1, stj, 1,	"STIJ")
cmdList.add_command(33,	-1, stz, 1,	"STIZ")
