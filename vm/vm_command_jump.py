from vm_word import Word
from vm_command import cmdList

#	Common jumps
def jmp(command, context):
	context.regs["J"].addr(context.get_reg_l().addr() + 1)
	return command.addr() + context.get_reg_index(command.index()).addr()

def jsj(command, context):
	return command.addr() + context.get_reg_index(command.index()).addr()

#	OF jumps
def jov(command, context):
	if context.flags["OF"]:
		context.flags["OF"] = 0
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

def jnov(command, context):
	if not context.flags["OF"]:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

#	CF jumps
def jl(command, context):
	if context.flags["CF"] < 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

def je(command, context):
	if context.flags["CF"] == 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def jg(command, context):
	if context.flags["CF"] > 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

def jge(command, context):
	if context.flags["CF"] >= 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def jne(command, context):
	if context.flags["CF"] != 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

def jle(command, context):
	if context.flags["CF"] <= 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
#	rA jumps
def jan(command, context):
	if context.regs["A"] < 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def jaz(command, context):
	if context.regs["A"] == 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

def jap(command, context):
	if context.regs["A"] > 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

def jann(command, context):
	if not context.regs["A"] < 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def janz(command, context):
	if not context.regs["A"] == 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def janp(command, context):
	if not context.regs["A"] > 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

#	rX jumps
def jxn(command, context):
	if context.regs["X"] < 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def jxz(command, context):
	if context.regs["X"] == 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

def jxp(command, context):
	if context.regs["X"] > 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

def jxnn(command, context):
	if not context.regs["X"] < 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def jxnz(command, context):
	if not context.regs["X"] == 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def jxnp(command, context):
	if not context.regs["X"] > 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

#	rI jumps
def jin(command, context):
	if context.get_reg_index(command.code() - 40) < 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def jiz(command, context):
	if context.get_reg_index(command.code() - 40) == 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def jip(command, context):
	if context.get_reg_index(command.code() - 40) > 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def jinn(command, context):
	if not context.get_reg_index(command.code() - 40) < 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

def jinz(command, context):
	if not context.get_reg_index(command.code() - 40) == 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1
	
def jinp(command, context):
	if not context.get_reg_index(command.code() - 40) > 0:
		return jmp(command, context)
	else:
		return context.get_reg_l().addr() + 1

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

cmdList.add_command(40, 0, jan,		1, "JAN")
cmdList.add_command(40, 1, jaz,		1, "JAZ")
cmdList.add_command(40, 2, jap,		1, "JAP")
cmdList.add_command(40, 3, jann,	1, "JANN")
cmdList.add_command(40, 4, janz,	1, "JANZ")
cmdList.add_command(40, 5, janp,	1, "JANP")

cmdList.add_command(47, 0, jxn,		1, "JXN")
cmdList.add_command(47, 1, jxz,		1, "JXZ")
cmdList.add_command(47, 2, jxp,		1, "JXP")
cmdList.add_command(47, 3, jxnn,	1, "JXNN")
cmdList.add_command(47, 4, jxnz,	1, "JXNZ")
cmdList.add_command(47, 5, jxnp,	1, "JXNP")

cmdList.add_command(41, 0, jin, 	1, "J1N")
cmdList.add_command(41, 1, jiz, 	1, "J1Z")
cmdList.add_command(41, 2, jip, 	1, "J1P")
cmdList.add_command(41, 3, jinn, 	1, "J1NN")
cmdList.add_command(41, 4, jinz, 	1, "J1NZ")
cmdList.add_command(41, 5, jinp, 	1, "J1NP")

cmdList.add_command(42, 0, jin, 	1, "J2N")
cmdList.add_command(42, 1, jiz, 	1, "J2Z")
cmdList.add_command(42, 2, jip, 	1, "J2P")
cmdList.add_command(42, 3, jinn, 	1, "J2NN")
cmdList.add_command(42, 4, jinz, 	1, "J2NZ")
cmdList.add_command(42, 5, jinp, 	1, "J2NP")

cmdList.add_command(43, 0, jin, 	1, "J3N")
cmdList.add_command(43, 1, jiz, 	1, "J3Z")
cmdList.add_command(43, 2, jip, 	1, "J3P")
cmdList.add_command(43, 3, jinn, 	1, "J3NN")
cmdList.add_command(43, 4, jinz, 	1, "J3NZ")
cmdList.add_command(43, 5, jinp, 	1, "J3NP")

cmdList.add_command(44, 0, jin, 	1, "J4N")
cmdList.add_command(44, 1, jiz, 	1, "J4Z")
cmdList.add_command(44, 2, jip, 	1, "J4P")
cmdList.add_command(44, 3, jinn, 	1, "J4NN")
cmdList.add_command(44, 4, jinz, 	1, "J4NZ")
cmdList.add_command(44, 5, jinp, 	1, "J4NP")

cmdList.add_command(45, 0, jin, 	1, "J5N")
cmdList.add_command(45, 1, jiz, 	1, "J5Z")
cmdList.add_command(45, 2, jip, 	1, "J5P")
cmdList.add_command(45, 3, jinn, 	1, "J5NN")
cmdList.add_command(45, 4, jinz, 	1, "J5NZ")
cmdList.add_command(45, 5, jinp, 	1, "J5NP")

cmdList.add_command(46, 0, jin, 	1, "J6N")
cmdList.add_command(46, 1, jiz, 	1, "J6Z")
cmdList.add_command(46, 2, jip, 	1, "J6P")
cmdList.add_command(46, 3, jinn, 	1, "J6NN")
cmdList.add_command(46, 4, jinz, 	1, "J6NZ")
cmdList.add_command(46, 5, jinp, 	1, "J6NP")