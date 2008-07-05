# read_mix.py

# read mix_lines from file

def line_parse(lines):
	for i in xrange(len(lines)):
		flag_has_label = lines[i][0].isalpha()
		split_line = lines[i].split()
		if( not lines[i][0].isalnum() ): # check if line hasn't label
			split_line.insert(0, None)
			
		# add None to end if label, mnemonic or operand missed
		while(len(split_line) < 3): 
			split_line.append(None)
			
		if(lines[i][0] == "*"):
			split_line = ["*", None, None]
		lines[i] = [split_line[0:3], i+1]
	return lines
	
def read(file):
	return line_parse(file.readlines())
