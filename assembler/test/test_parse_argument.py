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
      Line(None, "ALF", '"HEL 0"'),
      ['"', 'HEL 0', '"']
    )
    self.check_split(
      Line(None, "ALF", '"A B C D E F"'),
      ['"', 'A B C D E F', '"']
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
    self.assertEqual(parse_argument(Line(None, 'NOP', '-1*65,6(2:3)'), self.MockSymbolTable(), 0),
      Memory.mix2dec([-1, 1, 1, 6, 19, 0]))
    self.assertEqual(parse_argument(Line(None, 'NOP', 'SYM,5(1:1)'), self.MockSymbolTable(), 0),
      Memory.mix2dec([-1, 1, 59, 5, 9, 0]))
    self.assertEqual(parse_argument(Line(None, 'NOP', 'SYM,*/2(1:1)'), self.MockSymbolTable(), 10),
      Memory.mix2dec([-1, 1, 59, 5, 9, 0]))
    self.assertEqual(parse_argument(Line(None, 'STJ', 'SYM,*/2'), self.MockSymbolTable(), 10),
      Memory.mix2dec([-1, 1, 59, 5, 2, 0]))
    self.assertEqual(parse_argument(Line(None, 'STJ', None), self.MockSymbolTable(), 10),
      Memory.mix2dec([+1, 0, 0, 0, 2, 0]))
    self.assertEqual(parse_argument(Line(None, 'STJ', '(2:3)'), self.MockSymbolTable(), 10),
      Memory.mix2dec([+1, 0, 0, 0, 19, 0]))
    self.assertEqual(parse_argument(Line(None, 'STJ', ',*(2:3)'), self.MockSymbolTable(), 5),
      Memory.mix2dec([+1, 0, 0, 5, 19, 0]))

    self.assertRaises(ExpectedSExpError, parse_argument, Line(None, 'LDA', '+'), self.MockSymbolTable(), 0)
    self.assertRaises(ExpectedSExpError, parse_argument, Line(None, 'LDA', '+*-,2(5)'), self.MockSymbolTable(), 0)
    self.assertRaises(InvalidFieldSpecError, parse_argument, Line(None, 'LDA', '+*-2,2(-1)'), self.MockSymbolTable(), 0)
    self.assertRaises(InvalidAddrError, parse_argument, Line(None, 'LDA', '5000,2'), self.MockSymbolTable(), 0)
    self.assertRaises(InvalidIndError, parse_argument, Line(None, 'LDA', '2000,-1'), self.MockSymbolTable(), 0)
    self.assertRaises(UnexpectedStrInTheEndError, parse_argument, Line(None, 'LDA', 'LABB'), self.MockSymbolTable(), 0)
    self.assertRaises(UnexpectedStrInTheEndError, parse_argument, Line(None, 'LDA', '2+3(9)LABB'), self.MockSymbolTable(), 0)
    self.assertRaises(ExpectedExpError, parse_argument, Line(None, 'LDA', '2+3()'), self.MockSymbolTable(), 0)
    self.assertRaises(ExpectedExpError, parse_argument, Line(None, 'LDA', '2+3,(2)'), self.MockSymbolTable(), 0)
    self.assertRaises(ExpectedWExpError, parse_argument, Line(None, 'LDA', '='), self.MockSymbolTable(), 0)
    self.assertRaises(NoClosedBracketError, parse_argument, Line(None, 'LDA', '2+3(2'), self.MockSymbolTable(), 0)
    self.assertRaises(NoEqualSignError, parse_argument, Line(None, 'LDA', '=SYM*2+5'), self.MockSymbolTable(), 0)
    self.assertRaises(TooLongLiteralError, parse_argument, Line(None, 'LDA', '=1000000000='), self.MockSymbolTable(), 0)


  def test_directives(self):
    # test directives except "ALF"
    self.assertEqual(parse_argument(Line('LABEL', 'CON', '-**2+5/3(+2*8-1/5-1),64(4:5),2B(5:5)'), self.MockSymbolTable(), 1000),
      Memory.mix2dec([-1, 10, 25, 0, 1, 20]))
    self.assertEqual(parse_argument(Line('LABEL', 'CON', '1,-1000(0:2)'), self.MockSymbolTable(), 0),
      Memory.mix2dec([-1, 15, 40, 0, 0, 1]))
    self.assertEqual(parse_argument(Line('LABEL', 'CON', '***(***),-1000(0:2),1'), self.MockSymbolTable(), 0),
      Memory.mix2dec([+1, 0, 0, 0, 0, 1]))
    self.assertEqual(parse_argument(Line('LABEL', 'CON', '0'), self.MockSymbolTable(), 0),
      Memory.mix2dec([+1, 0, 0, 0, 0, 0]))
    self.assertEqual(parse_argument(Line('LABEL', 'CON', '2//3'), self.MockSymbolTable(), 0),
      Memory.mix2dec([+1, 42, 42, 42, 42, 42]))

    self.assertRaises(ExpectedSExpError, parse_argument, Line('LABEL', 'CON', '+'), self.MockSymbolTable(), 0)
    self.assertRaises(ExpectedSExpError, parse_argument, Line('LABEL', 'CON', '+SYM*'), self.MockSymbolTable(), 0)
    self.assertRaises(InvalidFieldSpecError, parse_argument, Line('LABEL', 'CON', '2+3(46)'), self.MockSymbolTable(), 0)
    self.assertRaises(InvalidFieldSpecError, parse_argument, Line('LABEL', 'CON', '2+3(3:2)'), self.MockSymbolTable(), 0)
    self.assertRaises(InvalidFieldSpecError, parse_argument, Line('LABEL', 'CON', '2+3(-1:2)'), self.MockSymbolTable(), 0)
    self.assertRaises(UnexpectedStrInTheEndError, parse_argument, Line('LABEL', 'CON', '2+3(45)666'), self.MockSymbolTable(), 0)
    self.assertRaises(ExpectedWExpError, parse_argument, Line('LABEL', 'CON', '?WHAT?'), self.MockSymbolTable(), 0)
    self.assertRaises(ExpectedExpError, parse_argument, Line('LABEL', 'CON', '2+3(?WHAT?)'), self.MockSymbolTable(), 0)
    self.assertRaises(ExpectedExpError, parse_argument, Line('LABEL', 'CON', '2+3(5),'), self.MockSymbolTable(), 0)
    self.assertRaises(NoClosedBracketError, parse_argument, Line('LABEL', 'CON', '2+3(5'), self.MockSymbolTable(), 0)


  def test_alf(self):
    self.assertEqual(parse_argument(Line(None, 'ALF', 'HELLO WORLD'), self.MockSymbolTable(), 0),
      135582544)
    self.assertEqual(parse_argument(Line(None, 'ALF', '"HELLO WORLD"'), self.MockSymbolTable(), 0),
      135582544)
    self.assertEqual(parse_argument(Line(None, 'ALF', '"HELL"'), self.MockSymbolTable(), 0),
      135582528)
    self.assertEqual(parse_argument(Line(None, 'ALF', 'HELL'), self.MockSymbolTable(), 0),
      135582528)
    self.assertEqual(parse_argument(Line(None, 'ALF', '"HELLO"'), self.MockSymbolTable(), 0),
      135582544)
    self.assertEqual(parse_argument(Line(None, 'ALF', 'HELLO%%%'), self.MockSymbolTable(), 0),
      135582544)

    self.assertRaises(UnquotedStringError, parse_argument, Line(None, 'ALF', '"FAIL'), self.MockSymbolTable(), 0)
    for s in "^ rh%% hell!".split():
      self.assertRaises(InvalidCharError, parse_argument, Line(None, 'ALF', s), self.MockSymbolTable(), 0)
    self.assertRaises(UnexpectedStrInTheEndError, parse_argument, Line(None, 'ALF', '"TEST"SMTH'), self.MockSymbolTable(), 0)


suite = unittest.makeSuite(ParseArgumentTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
