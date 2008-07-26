from vm_word import Word
from vm_command import cmdList

def lda(command, context):
	data = context.mem.get(command.M())
	context.rA = Word(data.int(command.F()))

def ldx(command, context):
	data = context.mem.get(command.M())
	context.rX = Word(data.int(command.F()))

def ldi(command, context):
	index = command.w_code() - 8
	data = context.mem.get(command.M())
	context.rI[index] = Word( data.int(command.F()) ).set_bytes([0,0,0], (1,3))

def ldan(command, context):
	data = context.mem.get(command.M())
	context.rA = Word( -data.int(command.F()) )

def ldxn(command, context):
	data = context.mem.get(command.M())
	context.rX = Word( -data.int(command.F()) )

def ldin(command, context):
	index = command.w_code() - 16
	data = context.mem.get(command.M())
	context.rI[index] = Word( -data.int(command.F()) ).set_bytes([0,0,0], (1,3))

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
