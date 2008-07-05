# mixm_asm.py

# Assembler - one of the parts of MixMachine,
# which assemles mix source code ("*.mix") to
# Mix Assembled code ("*.ma")

# Main module of assembler.
# Read two file names (gets by command line arguments):
# 1) input file (required)
# 2) output file (default "out.ma")

DEBUG = 1

import sys
from errors import *
import read_mix
import commands

DEFAULT_OUT_NAME = "out.ma"

	
#def write_mc(file, mem):
	## do nothing
	
	#mem_str = reduce(lambda x, y: x + "\n" + str(y), mem, str())
	#file.write(mem_str)

def print_src_debug(src):
	for item in src:
		print "%3i:  %10s  %4s  %s" % (item[1], item[0][0], item[0][1], item[0][2])

def print_cmds_debug(cmds):
	print "  OP  C  F    T description"
	print "---------------------------"
	for item in cmds:
		print "%4s %2i %2i %4s %s" % (cmds[item][1], cmds[item][0], cmds[item][2], cmds[item][3], cmds[item][4])

def main():
	arg_number = len(sys.argv) - 1
	if (arg_number < 1 or arg_number > 2):
		print ERR_INVALID_ARGS[1]
		return ERR_INVALID_ARGS[0]
	else:
		try:
			if (arg_number == 2):
				file_out = open(sys.argv[2], "w")
			else:
				file_out = open(DEFAULT_OUT_NAME, "w")
		except IOError, (errno, strerror):
			print strerror
			return ERR_INVALID_INPUT_FILE[0]
	try:
		file_in = open(sys.argv[1], "r")
	except IOError, (errno, strerror):
		print strerror
		return ERR_FILE[0]
		
	src = read_mix.read(file_in)
	if (DEBUG):
		print "SRC:"
		print_src_debug(src)
	file_in.close()
	
	cmds = commands.get_commands_op()
	if (DEBUG):
		print "CMDS:"
		print_cmds_debug(cmds)
	
	#write_mc(file_out, [23,453,124])
	file_out.close()
	
# if we executing module
if __name__ == '__main__':
	main()
