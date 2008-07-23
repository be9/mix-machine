import sys

class VMEvent(Exception):
	def __init__(self, desc):
		self.desc = desc
		
	def __str__(self):
		return "VMEvent: " + str(desc)
	
class VMStop(VMEvent):
	def __init__(self):
		self = VMEvent("stop")
		
class VMHalt(VMEvent):
	def __init__(self):
		self = VMEvent("halt")