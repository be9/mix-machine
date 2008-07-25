from vm_word import Word
from vm_command import cmdList

def sta(command, context):
	addr = command.addr() + context.get_reg_index(command.index()).int()
	word = context.mem.get(addr)
	F = divmod(command.fmt(), 8)
	
	bytes = context.regs["A"].get_bytes((5-F[1]+F[0],5))
	word.set_bytes(bytes, F)
	
	context.mem.set(word, addr)
	return context.get_reg_l().int() + 1

def stx(command, context):
	addr = command.addr() + context.get_reg_index(command.index()).int()
	word = context.mem.get(addr)
	F = divmod(command.fmt(), 8)
	
	bytes = context.regs["X"].get_bytes((5-F[1]+F[0],5))
	word.set_bytes(bytes, F)
	
	context.mem.set(word, addr)
	return context.get_reg_l().int() + 1

def sti(command, context):
	addr = command.addr() + context.get_reg_index(command.index()).int()
	word = context.mem.get(addr)
	F = divmod(command.fmt(), 8)
	
	bytes = context.get_reg_index(command.code() - 24)
	bytes.shift_l(3)
	word.set_bytes(bytes.get_bytes((2-F[1]+F[0], 2)), F)
	
	context.mem.set(word, addr)
	
	return context.get_reg_l().int() + 1

def stj(command, context):
	addr = command.addr() + context.get_reg_index(command.index()).int()
	word = context.mem.get(addr)
	F = divmod(command.fmt(), 8)
	
	bytes = context.regs["J"]
	bytes.shift_l(3)
	word.set_bytes(bytes.get_bytes((2-F[1]+F[0], 2)), F)
	
	context.mem.set(word, addr)
	
	return context.get_reg_l().int() + 1

def stz(command, context):
	addr = command.addr() + context.get_reg_index(command.index()).int()
	context.mem.set(Word(0), addr)
	return context.get_reg_l().int() + 1

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
