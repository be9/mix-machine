# operations.py

# File for creating dictionary with commands

class Op:
  def __init__(self, operation, c_code = None, f_code = None):
    self.operation = operation
    self.c_code = c_code
    self.f_code = f_code
  
  def __str__(self):
    return "%s %i %i" % (self.operation, self.c_code, self.f_code)

# operations dictionary with operation's mnemonic as a key

__instructions = {
"NOP" :   Op("NOP", 0, 0),
"ADD" :   Op("ADD", 1, 5),
"SUB" :   Op("SUB", 2, 5),
"MUL" :   Op("MUL", 3, 5),
"DIV" :   Op("DIV", 4, 5),
"NUM" :   Op("NUM", 5, 0),
"CHAR" :  Op("CHAR", 5, 1),
"HLT" :   Op("HLT", 5, 2),
"SLA" :   Op("SLA", 6, 0),
"SRA" :   Op("SRA", 6, 1),
"SLAX" :  Op("SLAX", 6, 2),
"SRAX" :  Op("SRAX", 6, 3),
"SLC" :   Op("SLC", 6, 4),
"SRC" :   Op("SRC", 6, 5),
"MOVE" :  Op("MOVE", 7, 1),
"LDA" :   Op("LDA", 8, 5),
"LD1" :   Op("LD1", 9, 5),
"LD2" :   Op("LD2", 10, 5),
"LD3" :   Op("LD3", 11, 5),
"LD4" :   Op("LD4", 12, 5),
"LD5" :   Op("LD5", 13, 5),
"LD6" :   Op("LD6", 14, 5),
"LDX" :   Op("LDX", 15, 5),
"LDAN" :  Op("LDAN", 16, 5),
"LD1N" :  Op("LD1N", 17, 5),
"LD2N" :  Op("LD2N", 18, 5),
"LD3N" :  Op("LD3N", 19, 5),
"LD4N" :  Op("LD4N", 20, 5),
"LD5N" :  Op("LD5N", 21, 5),
"LD6N" :  Op("LD6N", 22, 5),
"LDXN" :  Op("LDXN", 23, 5),
"STA" :   Op("STA", 24, 5),
"ST1" :   Op("ST1", 25, 5),
"ST2" :   Op("ST2", 26, 5),
"ST3" :   Op("ST3", 27, 5),
"ST4" :   Op("ST4", 28, 5),
"ST5" :   Op("ST5", 29, 5),
"ST6" :   Op("ST6", 30, 5),
"STX" :   Op("STX", 31, 5),
"STJ" :   Op("STJ", 32, 5),
"STZ" :   Op("STZ", 33, 5),
"JBUS" :  Op("JBUS", 34, 0),
"IOC" :   Op("IOC", 35, 0),
"IN" :    Op("IN", 36, 0),
"OUT" :   Op("OUT", 37, 0),
"JRED" :  Op("JRED", 38, 0),
"JMP" :   Op("JMP", 39, 0),
"JSJ" :   Op("JSJ", 39, 1),
"JOV" :   Op("JOV", 39, 2),
"JNOV" :  Op("JNOV", 39, 3),
"JL" :    Op("JL", 39, 4),
"JE" :    Op("JE", 39, 5),
"JG" :    Op("JG", 39, 6),
"JGE" :   Op("JGE", 39, 7),
"JNE" :   Op("JNE", 39, 8),
"JLE" :   Op("JLE", 39, 9),
"JAN" :   Op("JAN", 40, 0),
"JAZ" :   Op("JAZ", 40, 1),
"JAP" :   Op("JAP", 40, 2),
"JANN" :  Op("JANN", 40, 3),
"JANZ" :  Op("JANZ", 40, 4),
"JANP" :  Op("JANP", 40, 5),
"J1N" :   Op("J1N", 41, 0),
"J1Z" :   Op("J1Z", 41, 1),
"J1P" :   Op("J1P", 41, 2),
"J1NN" :  Op("J1NN", 41, 3),
"J1NZ" :  Op("J1NZ", 41, 4),
"JANP" :  Op("JANP", 41, 5),
"J2N" :   Op("J2N", 42, 0),
"J2Z" :   Op("J2Z", 42, 1),
"J2P" :   Op("J2P", 42, 2),
"J2NN" :  Op("J2NN", 42, 3),
"J2NZ" :  Op("J2NZ", 42, 4),
"J2NP" :  Op("J2NP", 42, 5),
"J3N" :   Op("J3N", 43, 0),
"J3Z" :   Op("J3Z", 43, 1),
"J3P" :   Op("J3P", 43, 2),
"J3NN" :  Op("J3NN", 43, 3),
"J3NZ" :  Op("J3NZ", 43, 4),
"J3NP" :  Op("J3NP", 43, 5),
"J4N" :   Op("J4N", 44, 0),
"J4Z" :   Op("J4Z", 44, 1),
"J4P" :   Op("J4P", 44, 2),
"J4NN" :  Op("J4NN", 44, 3),
"J4NZ" :  Op("J4NZ", 44, 4),
"J4NP" :  Op("J4NP", 44, 5),
"J5N" :   Op("J5N", 45, 0),
"J5Z" :   Op("J5Z", 45, 1),
"J5P" :   Op("J5P", 45, 2),
"J5NN" :  Op("J5NN", 45, 3),
"J5NZ" :  Op("J5NZ", 45, 4),
"J5NP" :  Op("J5NP", 45, 5),
"J6N" :   Op("J6N", 46, 0),
"J6Z" :   Op("J6Z", 46, 1),
"J6P" :   Op("J6P", 46, 2),
"J6NN" :  Op("J6NN", 46, 3),
"J6NZ" :  Op("J6NZ", 46, 4),
"J6NP" :  Op("J6NP", 46, 5),
"JXN" :   Op("JXN", 47, 0),
"JXZ" :   Op("JXZ", 47, 1),
"JXP" :   Op("JXP", 47, 2),
"JXNN" :  Op("JXNN", 47, 3),
"JXNZ" :  Op("JXNZ", 47, 4),
"JXNP" :  Op("JXNP", 47, 5),
"INCA" :  Op("INCA", 48, 0),
"DECA" :  Op("DECA", 48, 1),
"ENTA" :  Op("ENTA", 48, 2),
"ENNA" :  Op("ENNA", 48, 3),
"INC1" :  Op("INC1", 49, 0),
"DEC1" :  Op("DEC1", 49, 1),
"ENT1" :  Op("ENT1", 49, 2),
"ENN1" :  Op("ENN1", 49, 3),
"INC2" :  Op("INC2", 50, 0),
"DEC2" :  Op("DEC2", 50, 1),
"ENT2" :  Op("ENT2", 50, 2),
"ENN2" :  Op("ENN2", 50, 3),
"INC3" :  Op("INC3", 51, 0),
"DEC3" :  Op("DEC3", 51, 1),
"ENT3" :  Op("ENT3", 51, 2),
"ENN3" :  Op("ENN3", 51, 3),
"INC4" :  Op("INC4", 52, 0),
"DEC4" :  Op("DEC4", 52, 1),
"ENT4" :  Op("ENT4", 52, 2),
"ENN4" :  Op("ENN4", 52, 3),
"INC5" :  Op("INC5", 53, 0),
"DEC5" :  Op("DEC5", 53, 1),
"ENT5" :  Op("ENT5", 53, 2),
"ENN5" :  Op("ENN5", 53, 3),
"INC6" :  Op("INC6", 54, 0),
"DEC6" :  Op("DEC6", 54, 1),
"ENT6" :  Op("ENT6", 54, 2),
"ENN6" :  Op("ENN6", 54, 3),
"INCX" :  Op("INCX", 55, 0),
"DECX" :  Op("DECX", 55, 1),
"ENTX" :  Op("ENTX", 55, 2),
"ENNX" :  Op("ENNX", 55, 3),
"CMPA" :  Op("CMPA", 56, 5),
"CMP1" :  Op("CMP1", 57, 5),
"CMP2" :  Op("CMP2", 58, 5),
"CMP3" :  Op("CMP3", 59, 5),
"CMP4" :  Op("CMP4", 60, 5),
"CMP5" :  Op("CMP5", 61, 5),
"CMP6" :  Op("CMP6", 62, 5),
"CMPX" :  Op("CMPX", 63, 5)
}
__directives = ("EQU","ORIG","END","CON","ALF")


# real functions
__ops = dict(__instructions)

# directives
for s in __directives:
  __ops[s] = Op(s)


def get_codes(instruction):
  if is_instruction(instruction):
    instr = __instructions[instruction]
    return (instr.c_code, instr.f_code)
  else:
    return (None, None)

def is_valid_operation(operation):
  return operation.upper() in __ops

def is_instruction(operation):
  return operation.upper() in __instructions
