from copy import copy
from vm_errors import VMError

BYTE_SIZE = 6			# byte size in bits
MAX_BYTE = 2 ** BYTE_SIZE - 1	# maximum value of one byte
MAX_WORD = (MAX_BYTE+1) ** 5 - 1	# maximum value of one word

class WordError(VMError):
	pass

class Word:
	def __init__(self, obj):
		self.__val = [];
		
		if isinstance(obj, int):
			self.__val = self._int2val(obj)
			
		elif isinstance(obj, list) or isinstance(obj, tuple):
			self.__val = self._bytes2val(obj)
			
		elif isinstance(obj, float):
			self.__val = self._float2val(obj)
			
		elif isinstance(obj, str):
			self.__val = self.str2str(obj)
			
		elif isinstance(obj, Word):
			self.__val = copy(obj.__val)
			
		else:
			raise WordError("Incompartible type for 'Word' constructor")

	# convert different types into private data type
	def _int2val(self, int):
		if abs(int) > MAX_WORD:
			raise WordError("Integer initializator for 'Word' must be between -" + str(MAX_WORD) + " and " + str(MAX_WORD))
		if int >= 0:
			res = [1,0,0,0,0,0]
		else:
			res = [-1,0,0,0,0,0]
			
		for i in xrange(5, 0, -1):
			int, res[i] = divmod(abs(int), MAX_BYTE+1)
		return res

	def _bytes2val(self, bytes):
		if len(bytes) != 6:
			raise WordError("Bytes initializator for 'Word' must contain 6 bytes")
		if bytes[0] not in (1, -1):
			raise WordError("Bytes initializator for 'Word' must have first byte equal 1 or -1")
		for byte in bytes[1:6]:
			if not isinstance(byte, int) or byte > MAX_BYTE or byte < 0:
				raise WordError("Bytes initializator for 'Word' must have integer bytes between 0 and " + str(MAX_BYTE))
		return bytes
	
	def _float2val(self, float):
		return [1,0,0,0,0,0]
	def _str2val(self, str):
		return [1,0,0,0,0,0]

	# user operations with words
	def set_bytes(self, bytes, fmt=(0,5)):
		if not isinstance(fmt, list) and not isinstance(fmt, tuple) or (fmt[0] < 0 or fmt[1] < fmt[0] or fmt[1] > 5):
			raise WordError("Wrong format")
		if not isinstance(bytes, list) and not isinstance(bytes, tuple) or len(bytes) != fmt[1] - fmt[0] + 1:
			raise WordError("Bytes do not match to format")
		#self.__val[fmt[0]: fmt[1]+1] = bytes[0: fmt[1]-fmt[0]+1]
		self.__val = self._bytes2val(list(self.__val[0:fmt[0]] + bytes + self.__val[fmt[1] + 1: 6]))
		return self
	
	def get_bytes(self, fmt=(0,5)):
		if not isinstance(fmt, list) and not isinstance(fmt, tuple) or (fmt[0] < 0 or fmt[1] < fmt[0] or fmt[1] > 5):
			raise WordError("Wrong format")
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
		
	def __int__(self):
		return self.int()
	
	def __float__(self):
		return self.float()
	# debug
	def __str__(self):
		#return self.str()
		return str(self.__val)
	
	def shift_l(self, num=1, bytes=None):
		if num < 0:
			return self.shift_r(-num, bytes)
		elif num == 0:
			return []
		else:
			tmp = self.get_bytes((1,5))
			
			if num > 4:
				num = 5
			else:
				self.set_bytes(tmp[num: 5], (1,5-num))
			
			if bytes:
				self.set_bytes(bytes[0: num], (5-num+1, 5))
			else:
				self.set_bytes([0]*num, (5-num+1, 5))
			
			return tmp[0:num]
			
	def shift_r(self, num=1, bytes=None):
		if num < 0:
			return self.shift_l(-num, bytes)
		elif num == 0:
			return []
		else:
			tmp = self.get_bytes((1,5))
			
			if num > 4:
				num = 5
			else:
				self.set_bytes(tmp[0: 5-num], (num+1,5))
			
			if bytes:
				self.set_bytes(bytes[0: num], (1, num))
			else:
				self.set_bytes([0]*num, (1, num))
			
			return tmp[5-num: 5]
			
	def shift_cl(self, num=1):
		num %= 5
		self.shift_l(num, self.get_bytes((1,5)))
		return self
	
	def shift_cr(self, num=1):
		num %= 5
		self.shift_r(num, self.get_bytes((1,5))[5-num:])
		return self
	
	def addr(self, addr = None):
		if addr:
			self.set_addr(addr)
		return self.int((0,2))
	
	def code(self, code = None):
		if code:
			self.set_code(code)
		return self.int((5,5))
	
	def fmt(self, fmt = None):
		if fmt:
			self.set_fmt(fmt)
		return self.int((4,4))
		
	def index(self, index = None):
		if index:
			self.set_index(index)
		return self.int((3,3))
	
	def set_addr(self, addr):
		val = self._int2val(addr)
		self.set_bytes(val[4:6], (1,2))
		self.set_bytes(val[0:1], (0,0))
		return self
	
	def set_code(self, code):
		return self.set_bytes(code, (5,5))
	
	def set_fmt(self, fmt):
		return self.set_bytes(fmt, (4,4))
	
	def set_index(self, index):
		return self.set_bytes(index, (3,3))
	
	#def __neg__(self):
	#	return Word( [self.get_bytes((0,0))*-1, self.get_bytes((1,5))] )
	#def __pos__(self):
	#	return self
	#def __abs__(self):
	#	return Word( self.get_bytes((1,5)) )
		
	#def __add__(self, other):
	#	return Word(int(self) + int(other))
	#def __sub__(self, other):
	#def __mul__(self, other):
	#def __mod__(self, other):
	#def __divmod__(self, other):
	#def __lshift__(self, other):
	#def __rshift__(self, other):