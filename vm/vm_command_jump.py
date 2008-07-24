from vm_word import Word
from vm_command import cmdList

def jmp(command, context):
	return command.addr() + context.get_reg_index(command.index()).addr()
		
def jsj(command, context): pass
def jov(command, context): pass
def jnov(command, context): pass
def jl(command, context): pass
def je(command, context): pass
def jg(command, context): pass
def jge(command, context): pass
def jne(command, context): pass
def jle(command, context): pass

cmdList.add_command(39, 0, jmp,		1, "JMP")
cmdList.add_command(39, 1, jsj,		1, "JSJ")
cmdList.add_command(39, 2, jov,		1, "JOV")
cmdList.add_command(39, 3, jnov,	1, "JNOV")
cmdList.add_command(39, 4, jl,		1, "JL")
cmdList.add_command(39, 5, je,		1, "JE")
cmdList.add_command(39, 6, jg,		1, "JG")
cmdList.add_command(39, 7, jge,		1, "JGE")
cmdList.add_command(39, 8, jne,		1, "JNE")
cmdList.add_command(39, 9, jle,		1, "JLE")