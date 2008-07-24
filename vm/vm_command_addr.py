from vm_word import Word
from vm_command import cmdList

#def lda(command, context):
#	M = context.mem.get(command.addr() + context.get_reg_index(command.index()).int())
#	F = divmod(command.fmt(), 8)
#	context.regs["A"] = Word(M.int(F))
#	return context.get_reg_l().int() + 1

#cmdList.add_command(8,	-1, lda, 1,	"LDA")
