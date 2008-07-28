import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'vm'))
from vm_memory import *

class MemoryTestCase(unittest.TestCase):
	def setUp(self):
		pass
	
	def testConstructor(self):
		mem = Memory()
		
		self.assertEqual(len(mem.mem), MEM_SIZE)
		for i in mem.mem:
			self.assertEqual(i.int(), 0)
		
		self.assertNotEqual(mem.mem[0], mem.mem[1])	# !!

	def testChecks(self):
		mem = Memory()
		
		for i in xrange(0, MEM_SIZE):
			mem._check_addr(i)
				
		self.assertRaises(AddressOutOfRangeError, mem._check_addr, MEM_SIZE)
		self.assertRaises(AddressOutOfRangeError, mem._check_addr, -1)
		
		mem._check_range(0, MEM_SIZE-1)
		
		self.assertRaises(BadRangeError, mem._check_range, 0, 0)
		self.assertRaises(BadRangeError, mem._check_range, 1, 0)
		
		self.assertRaises(AddressOutOfRangeError, mem._check_range, -1, 0)
		self.assertRaises(AddressOutOfRangeError, mem._check_range, 0, MEM_SIZE)

	def testSet(self):
		mem = Memory()
		
		for i in xrange(0, MEM_SIZE):
			mem.set(i, i)
			
		for i in xrange(0, MEM_SIZE):
			self.assertEqual(mem.mem[i].int(), i)

		self.assertRaises(AddressOutOfRangeError, mem.set, MEM_SIZE, 1)
		self.assertRaises(AddressOutOfRangeError, mem.set, -1, 1)
		
	def testGet(self):
		mem = Memory()
		
		for i in xrange(0, MEM_SIZE):
			mem.set(i, i)
		
		for i in xrange(0, MEM_SIZE):
			self.assertEqual(mem.get(i).int(), i)

		self.assertRaises(AddressOutOfRangeError, mem.get, MEM_SIZE)
		self.assertRaises(AddressOutOfRangeError, mem.get, -1)
		
	def testSetRange(self):
		mem = Memory()
		
		mem.set_range(0, range(0, MEM_SIZE))
		
		for i in xrange(0, MEM_SIZE):
			self.assertEqual(mem.mem[i].int(), i)
		
		self.assertRaises(AddressOutOfRangeError, mem.set_range, -1, [1,2,3,4,5])
		self.assertRaises(AddressOutOfRangeError, mem.set_range, MEM_SIZE-1, [1,2,3,4,5])
		
		self.assertRaises(BadRangeError, mem.set_range, 0, [])
		
	def testGetRange(self):
		mem = Memory()
		
		mem.set_range(0, range(0, MEM_SIZE))

		get = mem.get_range(0, MEM_SIZE-1)
		
		for i in xrange(0, MEM_SIZE):
			self.assertEqual(get[i].int(), i)
		
		self.assertRaises(AddressOutOfRangeError, mem.get_range, -1, 0)
		self.assertRaises(AddressOutOfRangeError, mem.get_range, 0, MEM_SIZE)
		
		self.assertRaises(BadRangeError, mem.get_range, 0, 0)
		self.assertRaises(BadRangeError, mem.get_range, 1, 0)
		
	def testFill(self):
		mem = Memory()
		
		mem.fill(13)
		
		for i in mem.mem:
			self.assertEqual(i.int(), 13)

	def testLock(self):
		pass

suite = unittest.makeSuite(MemoryTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
