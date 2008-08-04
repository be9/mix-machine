import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'vm'))
from vm_memory import *

class MemoryTestCase(unittest.TestCase):
    def setUp(self):
        self.mem = Memory()
    
    def testConstructor(self):
        self.assertEqual(len(self.mem.mem), MEM_SIZE)
        for i in self.mem.mem:
            self.assertEqual(i.int(), 0)
        
        self.assertNotEqual(self.mem.mem[0], self.mem.mem[1])	# !!

    def testChecks(self):
        for i in xrange(0, MEM_SIZE):
            self.mem._check_addr(i)
                        
        self.assertRaises(AddressOutOfRangeError, self.mem._check_addr, MEM_SIZE)
        self.assertRaises(AddressOutOfRangeError, self.mem._check_addr, -1)
        
        self.mem._check_range(0, MEM_SIZE)
        
        self.assertRaises(BadRangeError, self.mem._check_range, 1, 0)
        
        self.assertRaises(AddressOutOfRangeError, self.mem._check_range, -1, 0)
        self.assertRaises(AddressOutOfRangeError, self.mem._check_range, 0, MEM_SIZE+1)

    def testSet(self):
        for i in xrange(0, MEM_SIZE):
            self.mem.set(i, i)
                
        for i in xrange(0, MEM_SIZE):
            self.assertEqual(self.mem.mem[i].int(), i)

        self.assertRaises(AddressOutOfRangeError, self.mem.set, MEM_SIZE, 1)
        self.assertRaises(AddressOutOfRangeError, self.mem.set, -1, 1)
            
    def testGet(self):
        for i in xrange(0, MEM_SIZE):
            self.mem.set(i, i)
        
        for i in xrange(0, MEM_SIZE):
            self.assertEqual(self.mem.get(i).int(), i)

        self.assertRaises(AddressOutOfRangeError, self.mem.get, MEM_SIZE)
        self.assertRaises(AddressOutOfRangeError, self.mem.get, -1)
        
    def testSetRange(self):
        self.mem.set_range(0, range(0, MEM_SIZE))
        
        for i in xrange(0, MEM_SIZE):
            self.assertEqual(self.mem.mem[i].int(), i)
        
        self.assertRaises(AddressOutOfRangeError, self.mem.set_range, -1, [1,2,3,4,5])
        self.assertRaises(AddressOutOfRangeError, self.mem.set_range, MEM_SIZE, [1,2,3,4,5])
            
    def testGetRange(self):
        self.mem.set_range(0, range(0, MEM_SIZE))

        get = self.mem.get_range(0, MEM_SIZE)
        
        for i in xrange(0, MEM_SIZE):
            self.assertEqual(get[i].int(), i)
        
        self.assertRaises(AddressOutOfRangeError, self.mem.get_range, -1, 0)
        self.assertRaises(AddressOutOfRangeError, self.mem.get_range, 0, MEM_SIZE+1)
        
        self.assertRaises(BadRangeError, self.mem.get_range, 1, 0)

    def testSetSlice(self):
        self.mem[0: MEM_SIZE] = range(0, MEM_SIZE)
        
        for i in xrange(0, MEM_SIZE):
            self.assertEqual(self.mem.mem[i].int(), i)

        self.mem[0:] = range(0, MEM_SIZE)
        
        for i in xrange(0, MEM_SIZE):
            self.assertEqual(self.mem.mem[i].int(), i)

        self.mem[:] = range(0, MEM_SIZE)
        
        for i in xrange(0, MEM_SIZE):
            self.assertEqual(self.mem.mem[i].int(), i)

        self.mem = Memory()
        self.mem[0: 100] = range(0, 100)
        
        for i in xrange(0, MEM_SIZE):
            if i < 100:
                self.assertEqual(self.mem.mem[i].int(), i)
            else:
                self.assertEqual(self.mem.mem[i].int(), 0)

        self.mem = Memory()
        self.mem[: 100] = range(0, 100)
        
        for i in xrange(0, MEM_SIZE):
            if i < 100:
                self.assertEqual(self.mem.mem[i].int(), i)
            else:
                self.assertEqual(self.mem.mem[i].int(), 0)
                        
        self.assertRaises(AddressOutOfRangeError, self.mem.__setslice__, -1, 4, [1,2,3,4,5])

        self.assertRaises(BadRangeError, self.mem.__setslice__, 1, 0, [])

    def testGetSlice(self):
        self.mem.set_range(0, range(0, MEM_SIZE))

        get = self.mem[0:0]
        self.assertEqual(get, [])

        get = self.mem[1:2]
        self.assertEqual(get[0].int(), 1)

        get = self.mem[:]
        
        for i in xrange(0, MEM_SIZE):
            self.assertEqual(get[i].int(), i)

        get = self.mem[:1]
        self.assertEqual(get[0].int(), 0)

        self.assertRaises(AddressOutOfRangeError, self.mem.__getslice__, -1, 4)

        self.assertRaises(BadRangeError, self.mem.__getslice__, 1, 0)

    def testGetItem(self):
        for i in xrange(0, MEM_SIZE):
            self.mem.set(i, i)
        
        for i in xrange(0, MEM_SIZE):
            self.assertEqual(self.mem[i].int(), i)

        self.assertRaises(AddressOutOfRangeError, self.mem.__getitem__, MEM_SIZE)
        self.assertRaises(AddressOutOfRangeError, self.mem.__getitem__, -1)
        
    def testSetItem(self):
        for i in xrange(0, MEM_SIZE):
            self.mem[i] = i
                
        for i in xrange(0, MEM_SIZE):
            self.assertEqual(self.mem.mem[i].int(), i)

        self.assertRaises(AddressOutOfRangeError, self.mem.__setitem__, MEM_SIZE, 1)
        self.assertRaises(AddressOutOfRangeError, self.mem.__setitem__, -1, 1)

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
