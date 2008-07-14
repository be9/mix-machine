
class Command:
	def __init__(self, code, func, time, label):
		self.code = int(code)
		self.time = int(time)
		self.func = func
		self.label = str(label)
		
	def __str__(self):
		return str(self.code) + ": " + str(self.label)

class CommandList:
	def __init__(self):
		self.commands = {}
	
	def add_command(self, code, func, time, label):
		self.commands[code] = Command(code, func, time, label)
	
	def get_command(self, code):
		try:
			ret = self.commands[code]
		except KeyError:
			return None
		
		return ret

cmdList = CommandList()