import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'vm2'))
from word import *
from errors import *

class WordTestCase(unittest.TestCase):
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
    for word_list, res in tests:
      self.assertEqual(Word.is_word_list(word_list), res)

  def testCommon(self):
    word = Word()
    self.assertEqual(word.word_list, [1, 0, 0, 0, 0, 0])
    word = Word([-1, 3, 63, 2, 8, 9])
    self.assertEqual(word.word_list, [-1, 3, 63, 2, 8, 9])
    word = Word(-1234567)
    self.assertEqual(word.word_list, [-1, 0, 4, 45, 26, 7])

    word = Word()
    word[3] = 5
    word[1] = 3
    word[0] = -1
    self.assertEqual(word, Word([-1, 3, 0, 5, 0, 0]))
    self.assertEqual(word[1], 3)
    self.assertEqual(word[5], 0)

    self.assertEqual(word[1:3], 3 * MAX_BYTE**2 + 5)
    self.assertEqual(word[0:3], -(3 * MAX_BYTE**2 + 5))
    self.assertEqual(word[:3], -(3 * MAX_BYTE**2 + 5))
    self.assertEqual(word[1:], 3 * MAX_BYTE**4 + 5 * MAX_BYTE**2)
    self.assertEqual(word[0:0], 0)

    word[1:1] = 4
    self.assertEqual(word, Word([-1, 4, 0, 5 ,0 ,0]))
    word[1:3] = 1 * MAX_BYTE**2 + 1
    self.assertEqual(word, Word([-1, 1, 0, 1 ,0 ,0]))
    word[0:3] = 1 * MAX_BYTE**2 + 1
    self.assertEqual(word, Word([+1, 1, 0, 1 ,0 ,0]))

    self.assertEqual(word[:], 1 * MAX_BYTE**4 + 1 * MAX_BYTE**2)


suite = unittest.makeSuite(WordTestCase, 'test')

if __name__ == "__main__":
  unittest.main()
