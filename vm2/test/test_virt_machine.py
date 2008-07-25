import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from virt_machine import *
from errors import *

class VMachineTestCase(unittest.TestCase):
  def testPositiveZero(self):
    self.assertEqual(VMachine.positive_zero(), [1, 0, 0, 0, 0, 0])



  def testCheckMemAddr(self):
    tests = [
      (0, True),
      (10, True),
      (MEMORY_SIZE - 1, True),
      (-1, False),
      (-10, False),
      (MEMORY_SIZE, False),
      (MEMORY_SIZE + 2, False),
    ]
    for addr, res in tests:
      self.assertEqual(VMachine.check_mem_addr(addr), res)

  def testCheckWord(self):
    tests = [
      ([+1,  0,  0,  0,  0,  0], True),
      ([-1, MAX_BYTE-1,  MAX_BYTE-1,  MAX_BYTE-1,  MAX_BYTE-1,  MAX_BYTE-1], True),
      ([+1, MAX_BYTE-1,  MAX_BYTE-1,  MAX_BYTE-1,  MAX_BYTE-1,  MAX_BYTE-1], True),
      ([-1, MAX_BYTE/2,  MAX_BYTE/2,  MAX_BYTE/2,  MAX_BYTE/2,  MAX_BYTE/2], True),
      ([+1, 0,  MAX_BYTE/2,  0,  MAX_BYTE/2,  0], True),
      ([+2,  0,  0,  0,  0,  0], False),
      ([-2,  0,  0,  0,  0,  0], False),
      ([-2,  0,  0, -1,  0,  0], False),
      ([+1,  0,  0, -1,  0,  0], False),
      ([-1, MAX_BYTE,  0,  0,  0,  0], False),
      ([1, 0,  0, 0,  0,  MAX_BYTE], False),
    ]
    for word, res in tests:
      self.assertEqual(VMachine.check_word(word), res)

  def testInit(self):
    tests = [
      (
        {
          155: ([+1, 0, 0, 0, 0, 0], 2),
          5: ([+1, 5, 50, 0, MAX_BYTE-1, 0], 2),
          MEMORY_SIZE-1: ([+1, 1, 1, 1, 1, 1], 2)
        },
        {
          5: [+1, 5, 50, 0, MAX_BYTE-1, 0],
          155: [+1, 0, 0, 0, 0, 0],
          MEMORY_SIZE-1: [+1, 1, 1, 1, 1, 1]
        },
        []
      ),
      (
        {
          155: ([+1, MAX_BYTE, 0, 0, 0, 0], 1),
          5: ([+1, 5, 50, 0, MAX_BYTE-1, 0], 2),
          MEMORY_SIZE+1: ([+1, 1, 1, 1, 1, 1], 3)
        },
        {
          5: [+1, 5, 50, 0, MAX_BYTE-1, 0]
        },
        [
          ( 1, InvalidMixWordError((1, MAX_BYTE, 0, 0, 0, 0)) ),
          ( 3, InvalidMemAddrError(MEMORY_SIZE+1) ),
        ]
      )
    ]
    for memory, memory_dict, errors in tests:
      vm = VMachine(memory)
      self.assertEqual(vm.errors, errors)
      self.assertTrue(vm.cmp_memory(memory_dict))

suite = unittest.makeSuite(VMachineTestCase, 'test')

if __name__ == "__main__":
  unittest.main()
