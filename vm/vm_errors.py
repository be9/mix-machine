import sys

class VMError(Exception):
	def __init__(self, err = ""):
		self.err = err
	def __str__(self):
		return str(self.err)
	def __cmp__(self, other):
		return cmp(self.err, other.err)
	
class VMRuntimeError(VMError):
	pass