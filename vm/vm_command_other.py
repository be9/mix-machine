from vm import VMContext
from vm_command import CommandList

class CommandOther:
	def __init__(self):
		# something like
		# command_list.add_command(0, 1, nop)
		# command_list.add_command(5, 0, hlt)
		pass
	
	# here go static functions
	def nop(context):
		pass 
	def hlt(context):
		pass 