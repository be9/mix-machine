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

def is_label(s):
	return s.isalnum() and any(ch.isalpha() for ch in s)
  
# returns Line object or None if text_line is empty or comment line
def parse_line(text_line):
	split_line = text_line.upper().split()
	
	# empty line or comment line
	if(len(split_line) == 0 or text_line[0] == '*'):
		return None
	
	result = Line()
	
	if( text_line[0].isalnum() ): # check if line has label
		if( is_label(split_line[0]) and len(split_line[0]) <= 10): # good label
			result.label = split_line[0]
		else:
			if(len(split_line[0]) > 10):
				raise AssemblySyntaxError("Very long name \"%s\" for label" % (split_line[0]))
			else:
				raise AssemblySyntaxError("Invalid name \"%s\" for label" % (split_line[0]))
		index = 1 # this is used later, operand in this case is second item in split_line
	else:
		result.label = None
		index = 0 # this is used later, operand in this case is first item in split_line
	
	if(split_line[0 + index] in mnemonics.cmds): # good operand
		result.operand = split_line[0+index]
	else:
		raise AssemblySyntaxError("Unknown operand \"%s\"" % (split_line[0 + index].upper()))
	if(len(split_line) > (1 + index)):
		result.address = split_line[1 + index] # no check of address
	else:
		result.address = None
	
	return result
