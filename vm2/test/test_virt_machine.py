import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from virt_machine import *
from word import *
from errors import *

class VMachineTestCase(unittest.TestCase):
  def testCheckMemAddr(self):
    tests = [
      (0, True),
      (10, True),
      (VMachine.MEMORY_SIZE - 1, True),
      (-1, False),
      (-10, False),
      (VMachine.MEMORY_SIZE, False),
      (VMachine.MEMORY_SIZE + 2, False),
    ]
    for addr, res in tests:
      self.assertEqual(VMachine.check_mem_addr(addr), res)

  def testInit(self):
    tests = [
      (
        {
          155: [+1, 0, 0, 0, 0, 0],
          5: [+1, 5, 50, 0, MAX_BYTE-1, 0],
          VMachine.MEMORY_SIZE-1: [+1, 1, 1, 1, 1, 1]
        },
        {
          5: Word([+1, 5, 50, 0, MAX_BYTE-1, 0]),
          155: Word([+1, 0, 0, 0, 0, 0]),
          VMachine.MEMORY_SIZE-1: Word([+1, 1, 1, 1, 1, 1])
        },
        []
      )
    ]
    for memory, memory_dict, errors in tests:
      vm = VMachine(memory, 0)
      self.assertEqual(vm.errors, errors)
      self.assertTrue(vm.cmp_memory(memory_dict))

suite = unittest.makeSuite(VMachineTestCase, 'test')

if __name__ == "__main__":
  unittest.main()
