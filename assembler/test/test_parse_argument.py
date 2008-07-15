# test_parse_argument.py

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_argument import *
from parse_line import Line

class ParseArgumentTestCase(unittest.TestCase):
  def check_split(self, line, tokens):
    parser = ArgumentParser(line, None, 0)
    self.assertEqual(parser.tokens, tokens)

  def test_split(self):
    self.check_split(
      Line(None, "NOP", "LABEL,3(3:5)"),
      ["LABEL", ",", "3", "(", "3", ":", "5", ")"]
    )
    self.check_split(
      Line(None, "NOP", "LAB*3**+5/7-4:5+234//12"),
      ["LAB", "*", "3", "*", "*", "+", "5", "/", "7", "-", "4", ":", "5", "+", "234", "//", "12"]
    )
    self.check_split(
      Line(None, "NOP", "***"),
      ["*", "*", "*"]
    )
    self.check_split(
      Line(None, "NOP", None),
      []
    )

  def test_basic(self):
    class MockSymbolTable:
      def find(self, arg, no):
        if arg == 'SYM':
          return 123
        elif arg == '1F':
          return 456
        elif arg == '1B':
          return 789
        elif arg == '2B':
          return 20
        else:
          return None

    # test NUMBER
    for i in (0, 123456, 64**5-1):
      #self.assertEqual(parse_argument(Line(None, 'NOP', str(i)), MockSymbolTable(), 0), i)
      self.assertEqual(parse_argument(Line(None, 'ORIG', str(i)), MockSymbolTable(), 0), i)

    # test SYMBOL
    #self.assertEqual(parse_argument(Line(None, 'NOP', 'SYM'), MockSymbolTable(), 0), 123)
    #self.assertEqual(parse_argument(Line(None, 'NOP', '1F'), MockSymbolTable(), 0), 456)
    self.assertEqual(parse_argument(Line(None, 'ORIG', '1F'), MockSymbolTable(), 0), 456)
    self.assertEqual(parse_argument(Line(None, 'ORIG', '1B'), MockSymbolTable(), 0), 789)

    # test CUR_ADDR
    for i in (0, 3, 2000, 3999):
      #self.assertEqual(parse_argument(Line(None, 'NOP', "*"), MockSymbolTable(), i), i)
      self.assertEqual(parse_argument(Line(None, 'ORIG', "*"), MockSymbolTable(), i), i)

    # test EXP
    #self.assertEqual(parse_argument(Line(None, 'NOP', "-1+5"), MockSymbolTable(), 0), 4)
    self.assertEqual(parse_argument(Line(None, 'ORIG', "-SYM+23*2/2B"), MockSymbolTable(), 0), -10)

    # test W_EXP (and F_PART)
    self.assertEqual(parse_argument(Line(None, 'ORIG', "65"),\
        MockSymbolTable(), 0), Memory.mix2dec([+1,0,0,0,1,1]))
    self.assertEqual(parse_argument(Line(None, 'ORIG', "65(1:2)"),\
        MockSymbolTable(), 0), Memory.mix2dec([+1,1,1,0,0,0]))
    self.assertEqual(parse_argument(Line(None, 'ORIG', "1(1:1),2(2:2),3(3:3),4(4:4),5(5:5)"),\
        MockSymbolTable(), 0), Memory.mix2dec([+1,1,2,3,4,5]))
    self.assertEqual(parse_argument(Line(None, 'ORIG', "1,-1000(0:2)"),\
        MockSymbolTable(), 0), Memory.mix2dec([-1,15,40,0,0,1]))
    self.assertEqual(parse_argument(Line(None, 'ORIG', "-1000(0:2),1"),\
        MockSymbolTable(), 0), Memory.mix2dec([+1,0,0,0,0,1]))

    # test nonsense
    #self.assertRaises(InvalidExpressionError, parse_argument, Line(None, 'NOP', 'QQQ'), MockSymbolTable(), 0)

suite = unittest.makeSuite(ParseArgumentTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
