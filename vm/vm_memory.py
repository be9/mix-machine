from vm_word import Word
from vm_errors import VMError
from copy import copy

MEM_SIZE = 4000	# memory size in words

class BadRangeError(VMError):
	def __init__(self, addr_b, addr_e):
		self = VMError("Bad addresses in range")
		self.addr_b = addr_b
		self.addr_e = addr_e

class BadRangeSizeError(VMError):
	def __init__(self, size_need, size_real):
		self = VMError("Size of given values do not match to range")
		self.size_need = size_need
		self.size_real = size_real
		
# runtime errors
class AddressOutOfRangeError(VMError):
	def __init__(self, addr):
		self = VMError("Adress out of range")
		self.addr = addr

class ReadLockedAddresError(VMError):
	def __init__(self, addr):
		self = VMError("Operating with locked memory")
		self.addr = addr

class Memory:
	def __init__(self):
		self.mem = [Word(0)]*MEM_SIZE
	
	def _check_addr(self, addr):
		if addr < 0 or addr > MEM_SIZE-1:
			raise AddressOutOfRangeError(addr)
	
	def _check_range(self, addr_b, addr_e):
		if addr_b >= addr_e:
			raise BadRangeError(addr_b, addr_e)
		if addr_b < 0:
			raise AddressOutOfRangeError(addr_b)
		elif addr_e > MEM_SIZE-1:
			raise AddressOutOfRangeError(addr_e)
	
	def set(self, val, addr):
		self._check_addr(addr)
		self.mem[addr] = Word(val)
	
	def get(self, addr):
		self._check_addr(addr)
		return self.mem[addr]
	
	def set_range(self, values, addr_b, addr_e = None):
		if not addr_e:
			addr_e = addr_b + len(values)
		self._check_range(addr_b, addr_e)
		
		if len(values) != addr_e - addr_b:
			raise BadRangeSizeError(addr_e - addr_b, len(values))
		self.mem[addr_b: addr_e] = [Word(val) for val in values]
	
	def get_range(self, addr_b, addr_e):
		self._check_range(addr_b, addr_e)
		return self.mem[addr_b: addr_e]
	
	def lock_range(self, addr_b, addr_e):
		pass
	def unlock_range(self, addr_b, addr_e):
		pass
	def unlock_all(self):
		pass
	def is_locked(self, addr_b, addr_e = None):
		pass
	
	def fill(self, val):
		self.mem = [Word(val)]*MEM_SIZE
			
	# debug
	def __str__(self):
		res = ""
		for i in self.mem:
			res += "\t" + str(i) + "\n"
		return res
		
	def str_range(self, addr_b, addr_e):
		self._check_range(addr_b, addr_e)
		
		res = ""
		for i in self.mem[addr_b: addr_e]:
			res += "\t" + str(i) + "\n"
		return res