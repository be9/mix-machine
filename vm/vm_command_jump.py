from vm_word import Word
from vm_command import cmdList

def jump(command, context):
	fmt = command.fmt()
	if fmt == 0:
		return jump_jmp(command, context)
	elif fmt == 1:
		return jump_jsj(command, context)
	elif fmt == 2:
		return jump_jov(command, context)
	elif fmt == 3:
		return jump_jnov(command, context)
	elif fmt == 4:
		return jump_jl(command, context)
	elif fmt == 5:
		return jump_je(command, context)
	elif fmt == 6:
		return jump_jg(command, context)
	elif fmt == 7:
		return jump_jge(command, context)
	elif fmt == 8:
		return jump_jne(command, context)
	elif fmt == 9:
		return jump_jle(command, context)
	else:
		return -1	# error invalid fmt

def jump_jmp(command, context):
	if command.index() == 0:
		return command.addr()
	else:
		return command.addr() + context.regs["I"+str(command.index())].addr()
		
def jump_jsj(command, context): pass
def jump_jov(command, context): pass
def jump_jnov(command, context): pass
def jump_jl(command, context): pass
def jump_je(command, context): pass
def jump_jg(command, context): pass
def jump_jge(command, context): pass
def jump_jne(command, context): pass
def jump_jle(command, context): pass

cmdList.add_command(39, jump, 1, "JMP, JSJ, JOV, JNOV, JL, JE, JG, JGE, JNE, JLE")