# parse_file.py

# read array of lines from file

from parse_line import *

def parse_lines(lines):
	errors = list() # array for (line_numbers, error_messages)
	result = list()
	for i in xrange(len(lines)):
		try:
			line = parse_line(lines[i])
		except AssemblySyntaxError, message:
			errors.append( (i, message) )
			continue
		if(line is None):
			continue
		line.line_number = i
		result.append(line)
	if(len(errors) > 0):
		return (0, errors)
	else:
		return (1, result)
	
def parse_file(file):
	return parse_lines(file.readlines())
