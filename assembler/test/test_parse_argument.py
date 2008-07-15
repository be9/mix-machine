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
    self.check_split(
      Line(None, "ALF", '"HELLO"'),
      ['"', 'HELLO', '"']
    )

  class MockSymbolTable:
    def find(self, arg, no):
      if arg == 'SYM':
        return -123
      elif arg == '1F':
        return 456
      elif arg == '1B':
        return 789
      elif arg == '2B':
        return 20
      else:
        return None

  def test_instructions(self):
    self.assertEqual(parse_argument(
      Line(None, 'NOP', '-1*65,6(2:3)'), self.MockSymbolTable(), 0),
      Memory.mix2dec([-1, 1, 1, 6, 19, 0])
    )
    self.assertEqual(parse_argument(
      Line(None, 'NOP', 'SYM,5(1:1)'), self.MockSymbolTable(), 0),
      Memory.mix2dec([-1, 1, 59, 5, 9, 0])
    )
    self.assertEqual(parse_argument(
      Line(None, 'NOP', 'SYM,*/2(1:1)'), self.MockSymbolTable(), 10),
      Memory.mix2dec([-1, 1, 59, 5, 9, 0])
    )

  def test_directives(self):
    # test directives except "ALF"
    self.assertEqual(parse_argument(
      Line('LABEL', 'CON', '-**2+5/3(+2*8-1/5-1),64(4:5),2B(5:5)'), self.MockSymbolTable(), 1000),
      Memory.mix2dec([-1, 10, 25, 0, 1, 20])
    )
    self.assertEqual(parse_argument(
      Line('LABEL', 'CON', '0'), self.MockSymbolTable(), 0),
      Memory.mix2dec([+1, 0, 0, 0, 0, 0])
    )

  def test_alf(self):
    self.assertEqual(parse_argument(
      Line(None, 'ALF', 'HELLO WORLD'), self.MockSymbolTable(), 1000),
      135582544
    )
    self.assertEqual(parse_argument(
      Line(None, 'ALF', '"HELLO WORLD"'), self.MockSymbolTable(), 1000),
      135582544
    )
    self.assertEqual(parse_argument(
      Line(None, 'ALF', '"HELL"'), self.MockSymbolTable(), 1000),
      135582528
    )
    self.assertEqual(parse_argument(
      Line(None, 'ALF', 'HELL'), self.MockSymbolTable(), 1000),
      135582528
    )
    self.assertEqual(parse_argument(
      Line(None, 'ALF', '"HELLO"'), self.MockSymbolTable(), 1000),
      135582544
    )
    self.assertEqual(parse_argument(
      Line(None, 'ALF', 'HELLO'), self.MockSymbolTable(), 1000),
      135582544
    )

  def test_errors(self):
    pass

suite = unittest.makeSuite(ParseArgumentTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
