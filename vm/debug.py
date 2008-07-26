from vm import VM
from vm_word import Word
from vm_command import cmdList
from vm_command_parser import ParsedCommand

from vm_memory import AddressOutOfRangeError
from vm_command import CommandNotFonudError
from vm_events import VMEvent, VMStop, VMHalt
from vm_errors import VMError, VMRuntimeError
from vm_command_parser import CommandInvalidIndexError, CommandInvalidFormatError



vm = VM()

vm.context.rI[1] = Word(10)

#		Addr	Index	Fmt	Code	# Offset	Asm
mem = [	Word([	1,0,18,	0,	5,	0]),	# 0		
	Word([	1,0,0,	1,	0,	39]),	# 1		
	Word([	1,0,18,	0,	5,	0]),	# 2		
	Word([	1,0,18,	0,	19,	0]),	# 3		
	Word([	1,0,0,	0,	0,	0]),	# 4		
	
	Word([	1,0,0,	0,	0,	0]),	# 5		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 6		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 7		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 8		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 9		NOP 
	
	Word([	1,0,0,	0,	0,	0]),	# 10		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 11		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 12		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 13		NOP 
	Word([	1,0,0,	0,	0,	0]),	# 14		NOP 
	
	Word([	1,0,19,	0,	0,	39]),	# 15		JMP 19
	Word([	1,0,0,	0,	0,	0]),	# 16		NOP 
	Word([	1,10,20,30,	40,	50]),	# 17		NOP 
	Word([	-1,1,2,	3,	4,	5]),	# 18		NOP 
	Word([	1,0,0,	0,	2,	5]),	# 19		HLT
	]

vm.context.mem.set_range(0, mem)
for i in vm.context.mem.get_range(0, 20):
	print str(i)

while not vm.context.is_halted:
	raw_input()
	
	print "--[trace]-----------------------------------------------"
	try:
		vm.trace()
	except:
		VMEvent
		
		AddressOutOfRangeError
		CommandNotFonudError
		
		VMError
		VMRuntimeError
		
		CommandInvalidIndexError
		CommandInvalidFormatError
		
		
	print str(vm.context)
	word = vm.context.mem.get(vm.context.rL.int())
	parsed_cmd = ParsedCommand(word, vm.context)
	print str(word) + ":\t" + str(cmdList.get_command(parsed_cmd.w_code(), parsed_cmd.w_fmt()))
	print "--------------------------------------------------------"