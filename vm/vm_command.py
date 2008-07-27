from vm_errors import VMError, VMRuntimeError

class Command:
	def __init__(self, code, fmt, func, time, label, is_jump):
		self.code = int(code)
		self.fmt = int(fmt)
		
		self.time = int(time)
		self.func = func
		self.label = str(label)
		
		self.is_jump = is_jump
		
	def __cmp__(self, other):
		if self.code == other.code:
			if self.fmt == -1 or other.fmt == -1:
				return 0
			elif self.fmt == other.fmt:
				return 0
			else:
				return 1
		else:
			return 1
		
	# debug
	def __str__(self):
		return str(self.code) + ":" + str(self.fmt) + " : " + str(self.label)

class CommandAlreadyExistError(VMError):
	pass

# runtime error
class CommandNotFoundError(VMRuntimeError):
	pass

class CommandList:
  def __init__(self):
    self.commands = {}
    self.multicodes = set()

  def add_command(self, code, fmt, func, time, label, is_jump = False):
    key = (code, fmt)

    if (code, -1) in self.commands or key in self.commands or \
        (code in self.multicodes and fmt == -1):
      raise CommandAlreadyExistError

    self.commands[key] = Command(code, fmt, func, time, label, is_jump)

    if fmt != -1:
      self.multicodes.add(code)

  def get_command(self, code, fmt = -1):
    if (code, fmt) in self.commands:
      return self.commands[(code, fmt)]
    elif (code, -1) in self.commands:
      return self.commands[(code, -1)]
    else:
      raise CommandNotFoundError

cmdList = CommandList()		# global command list, for adding commands
