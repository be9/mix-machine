from vm_errors import VMError

class Command:
	def __init__(self, code, fmt, func, time, label, is_jump):
		self.code = int(code)
		self.fmt = int(fmt)
		
		self.time = int(time)
		self.func = func
		self.label = str(label)
		
		self.is_jump = is_jump
		
	def __str__(self):
		return str(self.code) + ":" + str(self.fmt) + " : " + str(self.label)

class CommandListBadKeyError(VMError):
	def __init__(self, key):
		self = VMError("Invalid command key: (code, fmt)")
		self.key = key

class CommandList:
	def __init__(self):
		self.commands = {}
	
	def add_command(self, code, fmt, func, time, label, is_jump = False):
		key = (code, fmt)
		if self.commands.has_key(key):
			raise CommandListBadKeyError(key)
		
		self.commands[key] = Command(code, fmt, func, time, label, is_jump)
	
	def get_command(self, code, fmt = -1):
		key = (code, fmt)
		try:
			ret = self.commands[key]
		except KeyError:
			key = (code, -1)
			try:
				ret = self.commands[key]
			except KeyError:
				raise CommandListBadKeyError(key)
		
		return ret

cmdList = CommandList()