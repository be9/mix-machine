import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'vm2'))
from word_parser import *
from word import *
from virt_machine import *
from errors import *

class WordParserTestCase(unittest.TestCase):
  class MockVMachine:
    def __init__(self, word, r1 = None, r2 = None, r3 = None, r4 = None, r5 = None, r6 = None):
      self.word = Word(word)
      self.r0 = Word()
      self.r1 = Word(r1)
      self.r2 = Word(r2)
      self.r3 = Word(r3)
      self.r4 = Word(r4)
      self.r5 = Word(r5)
      self.r6 = Word(r6)
      self.of = False

    def reg(self, r):
      return self.__dict__["r" + r]

    def set_reg(self, r, w):
      self.__dict__["r" + r] = w

    def get_cur_word(self):
      return self.word

    @staticmethod
    def check_mem_addr(addr):
      return 0 <= addr < VMachine.MEMORY_SIZE

  def testGetSign(self):
    vmachine = self.MockVMachine(0)
    for sign in (-1, 1):
      vmachine.word = Word([sign, 44, 22, 0, 55, 1])
      self.assertEqual(WordParser.get_sign(vmachine), sign)
      vmachine.word = Word([sign, 0, 0, 0, 0, 0])
      self.assertEqual(WordParser.get_sign(vmachine), sign)

  def testGetFullAddr(self):
    vmachine = self.MockVMachine(
      0,
      71,
      -82,
      93,
      -104,
      115,
      126
    )

    tests = [
      ([+1,  0,  0,  0, 63, 63], 0),
      ([-1,  0,  0,  0, 63, 63], 0),
      ([-1,  0,  0,  1, 63, 63], 71),
      ([-1,  0,  0,  6, 63, 63], 126),
      ([-1,  0,  1,  6, 63, 63], 125),
      ([-1,  1,  1,  1, 63, 63], 6),
      ([+1,  1,  1,  1, 63, 63], 136),
    ]
    for word, addr in tests:
      vmachine.word = Word(word)
      self.assertEqual(WordParser.get_full_addr(vmachine), addr)
      self.assertEqual(vmachine.of, False)

    for word in ([1, 63, 63, 1, 0, 0], [-1, 63, 63, 2, 0, 0]):
      vmachine.of = False
      vmachine.word = Word(word)
      WordParser.get_full_addr(vmachine, True, False)
      self.assertEqual(vmachine.of, True)
    vmachine.of = False

    for word in ([1, 0, 0, 7, 0, 0], [1, 0, 0, 63, 0, 0]):
      vmachine.word = Word(word)
      self.assertRaises(InvalidIndError, WordParser.get_full_addr, vmachine)

    for word in ( [1, 62, 32, 0, 0, 0],
                  [1, 60, 45, 5, 0, 0],
                  [-1, 0, 1, 0, 0, 0],
                  [1, 0, 100, 4, 0, 0]):
      vmachine.word = Word(word)
      self.assertRaises(InvalidMemAddrError, WordParser.get_full_addr, vmachine, False, True)


  def testGetFieldSpec(self):
    vmachine = self.MockVMachine(0)

    tests = [
      (19, (2, 3)),
      ( 0, (0, 0)),
      (45, (5, 5)),
    ]
    for field, result in tests:
      vmachine.word = Word([1, 0, 0, 0, field, 0])
      self.assertEqual(WordParser.get_field_spec(vmachine), result)

    for field in (44, 6, 15, 46, 48 ):
      vmachine.word = Word([1, 0, 0, 0, field, 0])
      self.assertRaises(InvalidFieldSpecError, WordParser.get_field_spec, vmachine)

    for field in (0, 1, 10, 20, 33, 63):
      vmachine.word = Word([1, 0, 0, 0, field, 0])
      self.assertEqual(WordParser.get_field(vmachine), field)

suite = unittest.makeSuite(WordParserTestCase, 'test')

if __name__ == "__main__":
  unittest.main()
