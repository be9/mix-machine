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