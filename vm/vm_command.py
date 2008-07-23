from vm_errors import VMError

class Command:
	def __init__(self, code, func, time, label):
		self.code = int(code)
		self.time = int(time)
		self.func = func
		self.label = str(label)
		
	def __str__(self):
		return str(self.code) + ": " + str(self.label)

class CommandListBadCodeError(VMError):
	def __init__(self, code):
		self = VMError("Invalid command code")
		self.code = code

class CommandList:
	def __init__(self):
		self.commands = {}
	
	def add_command(self, code, func, time, label):
		if self.commands.has_key(code):
			raise CommandListBadCodeError(code)
		self.commands[code] = Command(code, func, time, label)
	
	def get_command(self, code):
		try:
			ret = self.commands[code]
		except KeyError:
			raise CommandListBadCodeError(code)
		
		return ret

cmdList = CommandList()