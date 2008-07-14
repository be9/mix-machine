# test_parse_argument.py

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_argument import *
from parse_line import Line

class ParseArgumentTestCase(unittest.TestCase):
  def check_split(self, line, tokens):
    parser = ArgumentParser(line, None)
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

  def test_parse_argument(self):
    class MockSymbolTable:
      def find(self, arg, no):
        if arg == 'SYM':
          return 123
        elif arg == '1F':
          return 456
        elif arg == '1B':
          return 789
        else:
          return None

    # test int
    #for i in (0, 123456, -123456, 64**5-1, -(64**5-1)):
      #self.assertEqual(parse_argument(Line(None, 'NOP', i), MockSymbolTable()), i)
    
    # test syms
    self.assertEqual(parse_argument(Line(None, 'NOP', 'SYM'), MockSymbolTable()), 123)
    self.assertEqual(parse_argument(Line(None, 'NOP', '1F'), MockSymbolTable()), 456)
    self.assertEqual(parse_argument(Line(None, 'NOP', '1B'), MockSymbolTable()), 789)

    # test nonsense
    #self.assertRaises(InvalidExpressionError, parse_argument, Line(None, 'NOP', 'QQQ'), MockSymbolTable())

suite = unittest.makeSuite(ParseArgumentTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
