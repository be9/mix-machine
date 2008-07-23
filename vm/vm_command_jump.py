from vm_word import Word
from vm_command import cmdList

def jmp(command, context):
	print "jmp: ", command
	return context.regs["L"] + 0

#cmdList.add_command(120, jmp, 1, "JMP")