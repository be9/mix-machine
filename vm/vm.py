
MEM_SIZE = 4000	# memory size in words
BYTE_SIZE = 6			# byte size in bits
MAX_BYTE = 2 ** BYTE_SIZE - 1	# maximum value of one byte
MAX_WORD = (MAX_BYTE+1) ** 5 - 1	# maximum value of one word

class Word:
	def __init__(self, obj):
		self.__val = [];
		
		if isinstance(obj, int):
			self.__val = self._int2val(obj)
			
		elif isinstance(obj, list):
			self.__val = self._bytes2val(obj)
			
		elif isinstance(obj, float):
			self.__val = self._float2val(obj)
			
		elif isinstance(obj, str):
			self.__val = self.str2str(obj)
			
		elif isinstance(obj, Word):
			self.__val = obj.__val
			
		else:
			pass	#error

	def _int2val(self, int):
		if int >= 0:
			res = [1,0,0,0,0,0]
		else:
			res = [-1,0,0,0,0,0]
			
		for i in xrange(5, 0, -1):
			int, res[i] = divmod(abs(int), MAX_BYTE+1)
		return res

	def _bytes2val(self, bytes):
		return bytes
	
	def _float2val(self, float):
		return [1,0,0,0,0,0]
	def _str2val(self, str):
		return [1,0,0,0,0,0]

	def set_bytes(self, bytes, fmt=(0,5)):
		self.__val[fmt[0]: fmt[1]+1] = bytes[0: fmt[1]-fmt[0]+1]
		pass
	
	def get_bytes(self, fmt=(0,5)):
		return self.__val[fmt[0]: fmt[1]+1]
	
	def int(self, fmt=(0,5)):
		res = 0;
		for i in xrange(max(fmt[0], 1), fmt[1]+1, 1):
			res = res*(MAX_BYTE+1) + self.__val[i]
		if fmt[0] == 0:
			res *= self.__val[0]
		return res
	
	def float(self):
		return 0.0
		
	def str(self):
		return "00000"
		
	#def __int__(self):
	#	return self.int();
	
		return "00000"
	
	# debug
	def __str__(self):
		return str(self.__val)

class VM:
	def __init__(self):
		self.regs = {	"A" :	Word(0),
							"X" : 	Word(0),
							"I1" :	Word(0),
							"I2" :	Word(0),
							"I3" :	Word(0),
							"I4" :	Word(0),
							"I5" :	Word(0),
							"I6" :	Word(0),
							"J" : 	Word(0),
							"L" :	Word(0) }
							
		self.flags = {  "OF" : 0,
							"CF" : 0 }
							
		self.mem = dict([ (i,Word(0)) for i in xrange(0, MEM_SIZE) ])
		
	# debug
	def __str__(self):
		return str(self.regs) + "\n"+  str(self.flags)
		
	def fill_memory(self, mem):
		for i in xrange(0, MEM_SIZE) :
			self.mem[i] = Word(mem[i])
			
	def dump_memory(self, begin, end):
		return [self.mem[i] for i in xrange(begin, end, 1)]
	
	def trace(self):
		pass
	
	def run(self):
		pass
		
	def reset(self):
		pass
	
	def set_brakepoint(self):
		pass
	def remove_brakepoint(self):
		pass
	def remove_all_brakepoints(self):
		pass
	def get_all_breakpoints(self):
		pass

pass
#mem = [Word(0)]*MEM_SIZE

#mem[0] = Word([1,2,3,4,5])
#mem[1] = Word([2,2,3,4,5])

#vm = VM()
#vm.fill_memory(mem)

#print [str(i) for i in vm.dump_memory(0, MEM_SIZE) ]
