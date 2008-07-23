from vm_word import Word
from vm_command import cmdList

#class CommandOther:
#	def __init__(self):
#		# something like
		# command_list.add_command(0, 1, nop)
		# command_list.add_command(5, 0, hlt)
#		pass
	
	# here go static functions
#	def nop(context):
#		pass 
#	def hlt(context):
#		pass 

def nop(command, context):
	print "NOP: ", command
	return context.regs["L"].addr() + 1
def spec(command, context):
	pass
	
cmdList.add_command(0, nop, 1, "NOP")
cmdList.add_command(112, spec, 1, "NUM, CHAR, HLT")