import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'vm2'))
from read_memory import *
from errors import *

class ReadMemoryTestCase(unittest.TestCase):
  def checkRaises(self, func, tests):
    """test = [ ( arg, error ), ...]"""
    for arg, error in tests:
      try:
        func(arg)
      except Exception, e:
        self.assertEqual(e, error)
      else:
        self.fail("Excepted error in '%s'" % arg)


  def testParse(self):
    tests_ok = [
        ( "100 1 0 0 0 0 1",    (100, [1, 0, 0, 0, 0, 1]) ),
        ( "55 -1 1 2 3 4 5 comment",    (55, [-1, 1, 2, 3, 4, 5]) ),
        ( "55\t\t-1 1\t2 3\t4 5 comment",    (55, [-1, 1, 2, 3, 4, 5]) ),
    ]
    for line, result in tests_ok:
      self.assertEqual(parse_word(line), result)

    test_raises = [
      ( "100 plus 1 2 3 4 5", InvalidIntError("plus") ),
      ( "100 +1 1 bug1 bug2 4 5", InvalidIntError("bug1") ),
      ( "100 +1 1 bug1 3 4", TooShortInputLineError("100 +1 1 bug1 3 4") ),
    ]
    self.checkRaises(parse_word, test_raises)


  def testReadNoErrors(self):
    # may be need more
    tests = [
      (
        [
          "123\n",
          "\n",
          "123 1\t\t0 0 0 5 2\n my comment",
          "120 1 1 2 3\t \t4 5 long comment\n",
          "   ",
          "3999 -1    63\t\t\t63 63\t63 63"
        ],
        (
          {
            120: [1, 1, 2, 3, 4, 5],
            123: [1, 0, 0, 0, 5, 2],
            3999: [-1, 63, 63, 63, 63, 63],
          },
          123,
          []
        )
      )
      #,
      #( lines, ( memory, start_address, errors) )
    ]
    for lines, res in tests:
      self.assertEqual(read_memory(lines), res)

  def testReadErrors(self):
    # errors of parse_word(...) see in testParse(...)
    tests = [
      (
        [
          "123WORD\n",
          "\n",
          "123 1\t\t0 0 0 5 \n my comment",
          "120 1 71 2 3\t \t4 5 long comment\n",
          "   ",
          "3999 -1    63\t\t\t63 63\t63 63",
          "3999 1    0\t\t0 0\t0 0",
          "5000 1 1 1 1 1 1"
        ],
        (
          {
            3999: [-1, 63, 63, 63, 63, 63],
          },
          None,
          [
            (1, InvalidStartAddressError("123WORD")),
            (3, InvalidIntError("my")),
            (4, InvalidMixWordError((1, 71, 2, 3, 4, 5))),
            (7, RepeatedAddressError(3999)),
            (8, InvalidMemAddrError(5000))
          ]
        )
      )
      #,
      #( lines, ( memory, start_address, errors) )
    ]
    for lines, res in tests:
      self.assertEqual(read_memory(lines), res)

suite = unittest.makeSuite(ReadMemoryTestCase, 'test')

if __name__ == "__main__":
  unittest.main()
