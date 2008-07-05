# commands.py

# File for creating dictionaris from commands.dat

# get commands dictionary with operand mnemonic like a key
def get_commands_op():
	result = dict()
	try:
		file = open("commands.dat")
	except IOError, (errno, strerror):
		return dict()
	for line in file.readlines():
		words = line.split()
		
		#empty line
		if(len(words) == 0):
			continue
		
		# comment line
		if (words[0][0] == '#'):
			continue
		
		# concat description words
		words[4] = " ".join(words[4:])
		words = words[0:5]
		
		# convert to int C, F
		words[0] = int(words[0])
		words[2] = int(words[2])
		
		# time - string, need more parse and depends on F value
		
		result[words[1]] = words
	file.close()
	return result
