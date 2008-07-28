from vm_word import Word
from vm_errors import VMError, VMRuntimeError
from copy import copy

MEM_SIZE = 4000	# memory size in words

class BadRangeError(VMError):
  pass

# runtime errors
class AddressOutOfRangeError(VMRuntimeError):
  pass

class Memory:
    def __init__(self):
        self.fill(0)

    @staticmethod
    def _check_addr(addr):
        if addr < 0 or addr > MEM_SIZE-1:
            raise AddressOutOfRangeError()

    @staticmethod
    def _check_range(addr_b, addr_e):
        if addr_b > addr_e:
            raise BadRangeError()
        if addr_b < 0:
            raise AddressOutOfRangeError()
        elif addr_e > MEM_SIZE:
            raise AddressOutOfRangeError()

    def set(self, addr, val):
        self._check_addr(addr)
        self.mem[addr] = Word(val)

    def get(self, addr):
        self._check_addr(addr)
        return self.mem[addr]

    def set_range(self, addr_b, values):
        addr_e = addr_b + len(values)
        self._check_range(addr_b, addr_e)
        self.mem[addr_b: addr_e] = [Word(values[i]) for i in xrange(len(values))]

    def get_range(self, addr_b, addr_e):
        self._check_range(addr_b, addr_e)
        return self.mem[addr_b: addr_e]

    def fill(self, val):
        self.mem = [Word(val) for _ in xrange(MEM_SIZE)]

    def __getslice__(self, a, b):
        b = min(MEM_SIZE, b)

        self._check_range(a, b)
        return self.mem[a: b]
        
    def __setslice__(self, a, b, seq):
        b = min(MEM_SIZE, b, a+len(seq))

        self._check_range(a, b)
        self.mem[a: b] = [Word(seq[i]) for i in xrange(len(seq))]

    def __getitem__(self, addr):
        self._check_addr(addr)
        return self.mem[addr]
    
    def __setitem__(self, addr, val):
        self._check_addr(addr)
        self.mem[addr] = Word(val)
