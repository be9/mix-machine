from vm_word import Word
from vm_command import cmdList

def cmpa(command, context):
	data = context.mem.get(command["M"])
	context.flags["CF"] = cmp(context.regs["A"].int(command["F"]), data.int(command["F"]))

def cmpx(command, context):
	data = context.mem.get(command["M"])
	context.flags["CF"] = cmp(context.regs["A"].int(command["F"]), data.int(command["F"]))

def cmpi(command, context):
	data = context.mem.get(command["M"])
	I = context.get_reg_index(command.code() - 56)
	context.flags["CF"] = cmp(I.regs["A"].int(command["F"]), data.int(command["F"]))

cmdList.add_command(56,	-1, cmpa, 1,	"CMPA")
cmdList.add_command(63,	-1, cmpx, 1,	"CMPX")

cmdList.add_command(57,	-1, cmpi, 1,	"CMP1")
cmdList.add_command(58,	-1, cmpi, 1,	"CMP2")
cmdList.add_command(59,	-1, cmpi, 1,	"CMP3")
cmdList.add_command(60,	-1, cmpi, 1,	"CMP4")
cmdList.add_command(61,	-1, cmpi, 1,	"CMP5")
cmdList.add_command(62,	-1, cmpi, 1,	"CMP6")
