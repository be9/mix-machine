# parse_line.py

# parse one source line

import mnemonics

class AssemblySyntaxError(Exception): pass

class Line:
	def __init__(self):
		self.label = None
		self.operand = None
		self.address = None
		self.line_number = None
	def __str__(self):
		return "%3i: %10s %4s %s" % (self.line_number, self.label, self.operand, self.address)

# returns Line object or None if text_line is empty or comment line
def parse_line(text_line):
	text_line = text_line.upper()
	
	split_line = text_line.split()
	
	# empty line or comment line
	if(len(split_line) == 0 or text_line[0] == '*'):
		return None
	
	result = Line()
	
	if( text_line[0].isalnum() ): # check if line hasn't label
		if( split_line[0].isalnum() and len(split_line[0]) <= 10): # good label
			result.label = split_line[0]
		else:
			if(len(split_line[0]) > 10):
				raise AssemblySyntaxError("Very long name \"%s\" for label" % (split_line[0]))
			else:
				raise AssemblySyntaxError("Invalid name \"%s\" for label" % (split_line[0]))
		if(split_line[1] in mnemonics.cmds): # good operand
			result.operand = split_line[1]
		else:
			raise AssemblySyntaxError("Unknown operand \"%s\"" % (split_line[1].upper()))
		if(len(split_line) > 2):
			result.address = split_line[2] # no check of address
		else:
			result.address = None
	else:
		result.label = None
		if(split_line[0] in mnemonics.cmds): # good operand
			result.operand = split_line[0]
		else:
			raise AssemblySyntaxError("Unknown operand \"%s\"" % (split_line[0].upper()))
		if(len(split_line) > 1):
			result.address = split_line[1] # no check of address
		else:
			result.address = None
	return result
