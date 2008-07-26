from vm_word import Word
from vm_errors import VMError, VMRuntimeError
from copy import copy

MEM_SIZE = 4000	# memory size in words

class BadRangeError(VMError):
	pass

class BadRangeSizeError(VMError):
	pass
		
# runtime errors
class AddressOutOfRangeError(VMRuntimeError):
	pass

class ReadLockedAddresError(VMRuntimeError):
	pass

class Memory:
	def __init__(self):
		self.mem = [Word(0) for i in xrange(0, MEM_SIZE)]
	
	@staticmethod
	def _check_addr(addr):
		if addr < 0 or addr > MEM_SIZE-1:
			raise AddressOutOfRangeError(addr)
		return True
	
	@staticmethod
	def _check_range(addr_b, addr_e):
		if addr_b >= addr_e:
			raise BadRangeError()
		if addr_b < 0:
			raise AddressOutOfRangeError()
		elif addr_e > MEM_SIZE-1:
			raise AddressOutOfRangeError()
		return True
	
	def set(self, addr, val):
		self._check_addr(addr)
		self.mem[addr] = Word(val)
	
	def get(self, addr):
		self._check_addr(addr)
		return self.mem[addr]
	
	def set_range(self, addr_b, values):
		addr_e = addr_b + len(values) -1
		self._check_range(addr_b, addr_e)
		self.mem[addr_b: addr_e] = [Word(values[i]) for i in xrange(0, len(values))]
	
	def get_range(self, addr_b, addr_e):
		self._check_range(addr_b, addr_e)
		return self.mem[addr_b: addr_e+1]
	
	def lock_range(self, addr_b, addr_e):
		pass
	def unlock_range(self, addr_b, addr_e):
		pass
	def unlock_all(self):
		pass
	def is_locked(self, addr_b, addr_e = None):
		pass
	
	def fill(self, val):
		self.mem = [Word(val) for i in xrange(0, MEM_SIZE)]
			
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