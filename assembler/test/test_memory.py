# test_memory.py

# module for testing class Memory and functions mix2dec, dec2mix

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_line import *
from memory import *

class MemoryTestCase(unittest.TestCase):
  def checkWords(self, word1, word2):
    if word1[1:] != [0, 0, 0, 0, 0]:
      self.assertEqual(word1,word2)
    else:
      self.assertEqual([0, 0, 0, 0, 0], word2[1:])

  def testConvert(self):
    tests = [ # pairs (mix_word, decimal)
      ([+1,  0,  0,  0,  0,  1], 1),
      ([+1,  0,  0,  1,  0,  0], 4096),
      ([-1,  0,  0,  1,  0,  0], -4096),
      ([-1,  1,  2,  3,  4,  5], -17314053),
      ([+1, 63, 62, 61, 60,  0], 1073471232),
      ([+1,  0,  0,  0,  0,  0], 0),
      ([-1,  0,  0,  0,  0,  0], 0),
      ([-1,  0,  0,  0,  0,  0], -0),
      ([+1,  0,  0,  0,  0,  0], -0)
    ]
    for word, dec in tests:
      self.assertEqual(Memory.mix2dec(word), dec)
      self.checkWords(Memory.dec2mix(dec), word)

  def testMemory_set_byte(self):
    memory = Memory()
    byte_tests = [ # (word_index, byte_index, value, word)
      (113, 3, 45, [+1, 0, 0, 45, 0, 0]),
      (0, 0, -1, [-1, 0, 0, 0, 0, 0]),
      (3999, 5, 63, [+1, 0, 0, 0, 0, 63])
    ]
    for word_index, byte_index, value, word in byte_tests:
      memory.set_byte(word_index, byte_index, value)
      self.assertEqual(memory.memory[word_index], word)

  def testMemory_set_instruction(self):
    memory = Memory()
    instruction_tests = [ # (word_index, a_code, i_code, f_code, c_code, word)
      (0, -0, 0, 0, 0, [+1, 0, 0, 0, 0, 0]),
      (3999, -113, 43, 22, 62, [-1, 1, 49, 43, 22, 62]),
      (3999, +113, 62, 22, 43, [+1, 1, 49, 62, 22, 43]),
    ]
    for word_index, a_code, i_code, f_code, c_code, word in instruction_tests:
      memory.set_instruction(word_index, a_code, i_code, f_code, c_code)
      self.assertEqual(memory.memory[word_index], word)

  def testMemory_set_word(self):
    memory = Memory()
    value_tests = [ # (word_index, value, word)
      (0, 1073471232, [+1, 63, 62, 61, 60, 00]),
      (3999, -113, [-1, 0, 0, 0, 1, 49]),
      (3999, +113, [+1, 0, 0, 0, 1, 49]),
    ]
    for word_index, value, word in value_tests:
      memory.set_word(word_index, value)
      self.assertEqual(memory.memory[word_index], word)

  def testMemory_cmp_memory(self):
    memory = Memory()
    test = ( # pairs (value, addr)
      (1,           0),
      (4096,        33),
      (-4096,       77),
      (-17314053,   999),
      (1073471232,  2000),
      (0,           3998),
      (64,          3999)
    )
    memory_part = {
      0:    [+1,  0,  0,  0,  0,  1],
      1:    [+1,  0,  0,  0,  0,  0],
      33:   [+1,  0,  0,  1,  0,  0],
      77:   [-1,  0,  0,  1,  0,  0],
      999:  [-1,  1,  2,  3,  4,  5],
      2000: [+1, 63, 62, 61, 60,  0],
      3998: [+1,  0,  0,  0,  0,  0],
      3999: [+1,  0,  0,  0,  1,  0]
    }
    for value, addr in test:
      memory.set_word(addr, value)
    self.assertTrue(memory.cmp_memory(memory_part))


    memory = Memory()
    test = ( # pairs (value, addr)
      (1,           0),
      (4096,        33),
      (-4096,       77),
      (-17314053,   999),
      (1073471232,  2000),
      (0,           3998),
      (64,          3999)
    )
    memory_part_1 = { # odd word#1
      0:    [+1,  0,  0,  0,  0,  1],
      1:    [+1,  0, 11, 11, 11, 11],
      33:   [+1,  0,  0,  1,  0,  0],
      77:   [-1,  0,  0,  1,  0,  0],
      999:  [-1,  1,  2,  3,  4,  5],
      2000: [+1, 63, 62, 61, 60,  0],
      3998: [+1,  0,  0,  0,  0,  0],
      3999: [+1,  0,  0,  0,  1,  0]
    }
    memory_part_2 = { # no word#33
      0:    [+1,  0,  0,  0,  0,  1],
      77:   [-1,  0,  0,  1,  0,  0],
      999:  [-1,  1,  2,  3,  4,  5],
      2000: [+1, 63, 62, 61, 60,  0],
      3998: [+1,  0,  0,  0,  0,  0],
      3999: [+1,  0,  0,  0,  1,  0]
    }
    for value, addr in test:
      memory.set_word(addr, value)

    self.assertFalse(memory.cmp_memory(memory_part_1))
    self.assertFalse(memory.cmp_memory(memory_part_2))

suite = unittest.makeSuite(MemoryTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
