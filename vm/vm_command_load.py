from vm_word import Word
from vm_command import cmdList

def lda(command, context):
	M = context.mem.get(command.addr() + context.get_reg_index(command.index()).int())
	F = divmod(command.fmt(), 8)
	context.regs["A"] = Word(M.int(F))
	return context.get_reg_l().int() + 1

def ldx(command, context):
	M = context.mem.get(command.addr() + context.get_reg_index(command.index()).int())
	F = divmod(command.fmt(), 8)
	context.regs["X"] = Word(M.int(F))
	return context.get_reg_l().int() + 1

def ldi(command, context):
	M = context.mem.get(command.addr() + context.get_reg_index(command.index()).int())
	F = divmod(command.fmt(), 8)
	context.set_reg_index(command.code() - 8, Word(M.int(F)).set_bytes([0,0,0], (1,3)))
	return context.get_reg_l().int() + 1

def ldan(command, context):
	M = context.mem.get(command.addr() + context.get_reg_index(command.index()).int())
	F = divmod(command.fmt(), 8)
	context.regs["A"] = Word(-M.int(F))
	return context.get_reg_l().int() + 1

def ldxn(command, context):
	M = context.mem.get(command.addr() + context.get_reg_index(command.index()).int())
	F = divmod(command.fmt(), 8)
	context.regs["X"] = Word(-M.int(F))
	return context.get_reg_l().int() + 1

def ldin(command, context):
	M = context.mem.get(command.addr() + context.get_reg_index(command.index()).int())
	F = divmod(command.fmt(), 8)
	context.set_reg_index(command.code() - 16, Word(-M.int(F)).set_bytes([0,0,0], (1,3)))
	return context.get_reg_l().int() + 1

cmdList.add_command(8,	-1, lda, 1,	"LDA")
cmdList.add_command(15,	-1, ldx, 1,	"LDX")

cmdList.add_command(9,	-1, ldi, 1,	"LD1")
cmdList.add_command(10,	-1, ldi, 1,	"LD2")
cmdList.add_command(11,	-1, ldi, 1,	"LD3")
cmdList.add_command(12,	-1, ldi, 1,	"LD4")
cmdList.add_command(13,	-1, ldi, 1,	"LD5")
cmdList.add_command(14,	-1, ldi, 1,	"LD6")

cmdList.add_command(16,	-1, ldan, 1,	"LDAN")
cmdList.add_command(23,	-1, ldxn, 1,	"LDXN")

cmdList.add_command(17,	-1, ldin, 1,	"LD1N")
cmdList.add_command(18,	-1, ldin, 1,	"LD2N")
cmdList.add_command(19,	-1, ldin, 1,	"LD3N")
cmdList.add_command(20,	-1, ldin, 1,	"LD4N")
cmdList.add_command(21,	-1, ldin, 1,	"LD5N")
cmdList.add_command(22,	-1, ldin, 1,	"LD6N")
