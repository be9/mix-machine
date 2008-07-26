from vm_word import Word
from vm_command import cmdList

#	Common jumps
def jmp(cmd, context):
	context.rJ = Word(context.rL.int() + 1)
	context.rL = Word(cmd.M())

def jsj(command, context):
	context.rL = Word(cmd.M())

#	OF jumps
def jov(command, context):
	if context.OF:
		context.OF = 0
		jmp(command, context)

def jnov(command, context):
	if not context.OF:
		jmp(command, context)

#	CF jumps
def jl(command, context):
	if context.CF < 0:
		jmp(command, context)

def je(command, context):
	if context.CF == 0:
		jmp(command, context)
	
def jg(command, context):
	if context.CF > 0:
		jmp(command, context)

def jge(command, context):
	if context.CF >= 0:
		jmp(command, context)
	
def jne(command, context):
	if context.CF != 0:
		jmp(command, context)
		
def jle(command, context):
	if context.CF <= 0:
		jmp(command, context)
	
#	rA jumps
def jan(command, context):
	if context.rA < 0:
		jmp(command, context)
	
def jaz(command, context):
	if context.rA == 0:
		jmp(command, context)

def jap(command, context):
	if context.rA > 0:
		jmp(command, context)

def jann(command, context):
	if not context.rA < 0:
		jmp(command, context)
	
def janz(command, context):
	if not context.rA == 0:
		jmp(command, context)
	
def janp(command, context):
	if not context.rA > 0:
		jmp(command, context)

#	rX jumps
def jxn(command, context):
	if context.rX < 0:
		jmp(command, context)
	
def jxz(command, context):
	if context.rX == 0:
		jmp(command, context)

def jxp(command, context):
	if context.rX > 0:
		jmp(command, context)

def jxnn(command, context):
	if not context.rX < 0:
		jmp(command, context)
	
def jxnz(command, context):
	if not context.rX == 0:
		jmp(command, context)
	
def jxnp(command, context):
	if not context.rX > 0:
		jmp(command, context)

#	rI jumps
def jin(command, context):
	if context.rI[command.w_code() - 40] < 0:
		jmp(command, context)
	
def jiz(command, context):
	if context.rI[command.w_code() - 40] == 0:
		jmp(command, context)
	
def jip(command, context):
	if context.rI[command.w_code() - 40] > 0:
		jmp(command, context)

def jinn(command, context):
	if not context.rI[command.w_code() - 40] < 0:
		jmp(command, context)

def jinz(command, context):
	if not context.rI[command.w_code() - 40] == 0:
		jmp(command, context)

def jinp(command, context):
	if not context.rI[command.w_code() - 40] > 0:
		jmp(command, context)

cmdList.add_command(39, 0, jmp,		1, "JMP",	True)
cmdList.add_command(39, 1, jsj,		1, "JSJ", 	True)
cmdList.add_command(39, 2, jov,		1, "JOV", 	True)
cmdList.add_command(39, 3, jnov,	1, "JNOV", 	True)
cmdList.add_command(39, 4, jl,		1, "JL", 	True)
cmdList.add_command(39, 5, je,		1, "JE", 	True)
cmdList.add_command(39, 6, jg,		1, "JG", 	True)
cmdList.add_command(39, 7, jge,		1, "JGE", 	True)
cmdList.add_command(39, 8, jne,		1, "JNE", 	True)
cmdList.add_command(39, 9, jle,		1, "JLE", 	True)

cmdList.add_command(40, 0, jan,		1, "JAN", 	True)
cmdList.add_command(40, 1, jaz,		1, "JAZ", 	True)
cmdList.add_command(40, 2, jap,		1, "JAP", 	True)
cmdList.add_command(40, 3, jann,	1, "JANN", 	True)
cmdList.add_command(40, 4, janz,	1, "JANZ", 	True)
cmdList.add_command(40, 5, janp,	1, "JANP", 	True)

cmdList.add_command(47, 0, jxn,		1, "JXN", 	True)
cmdList.add_command(47, 1, jxz,		1, "JXZ", 	True)
cmdList.add_command(47, 2, jxp,		1, "JXP", 	True)
cmdList.add_command(47, 3, jxnn,	1, "JXNN", 	True)
cmdList.add_command(47, 4, jxnz,	1, "JXNZ", 	True)
cmdList.add_command(47, 5, jxnp,	1, "JXNP", 	True)

cmdList.add_command(41, 0, jin, 	1, "J1N", 	True)
cmdList.add_command(41, 1, jiz, 	1, "J1Z", 	True)
cmdList.add_command(41, 2, jip, 	1, "J1P", 	True)
cmdList.add_command(41, 3, jinn, 	1, "J1NN", 	True)
cmdList.add_command(41, 4, jinz, 	1, "J1NZ", 	True)
cmdList.add_command(41, 5, jinp, 	1, "J1NP", 	True)

cmdList.add_command(42, 0, jin, 	1, "J2N", 	True)
cmdList.add_command(42, 1, jiz, 	1, "J2Z", 	True)
cmdList.add_command(42, 2, jip, 	1, "J2P", 	True)
cmdList.add_command(42, 3, jinn, 	1, "J2NN", 	True)
cmdList.add_command(42, 4, jinz, 	1, "J2NZ", 	True)
cmdList.add_command(42, 5, jinp, 	1, "J2NP", 	True)

cmdList.add_command(43, 0, jin, 	1, "J3N", 	True)
cmdList.add_command(43, 1, jiz, 	1, "J3Z", 	True)
cmdList.add_command(43, 2, jip, 	1, "J3P", 	True)
cmdList.add_command(43, 3, jinn, 	1, "J3NN", 	True)
cmdList.add_command(43, 4, jinz, 	1, "J3NZ", 	True)
cmdList.add_command(43, 5, jinp, 	1, "J3NP", 	True)

cmdList.add_command(44, 0, jin, 	1, "J4N", 	True)
cmdList.add_command(44, 1, jiz, 	1, "J4Z", 	True)
cmdList.add_command(44, 2, jip, 	1, "J4P", 	True)
cmdList.add_command(44, 3, jinn, 	1, "J4NN", 	True)
cmdList.add_command(44, 4, jinz, 	1, "J4NZ", 	True)
cmdList.add_command(44, 5, jinp, 	1, "J4NP", 	True)

cmdList.add_command(45, 0, jin, 	1, "J5N", 	True)
cmdList.add_command(45, 1, jiz, 	1, "J5Z", 	True)
cmdList.add_command(45, 2, jip, 	1, "J5P", 	True)
cmdList.add_command(45, 3, jinn, 	1, "J5NN", 	True)
cmdList.add_command(45, 4, jinz, 	1, "J5NZ", 	True)
cmdList.add_command(45, 5, jinp, 	1, "J5NP", 	True)

cmdList.add_command(46, 0, jin, 	1, "J6N", 	True)
cmdList.add_command(46, 1, jiz, 	1, "J6Z", 	True)
cmdList.add_command(46, 2, jip, 	1, "J6P", 	True)
cmdList.add_command(46, 3, jinn, 	1, "J6NN", 	True)
cmdList.add_command(46, 4, jinz, 	1, "J6NZ", 	True)
cmdList.add_command(46, 5, jinp, 	1, "J6NP", 	True)