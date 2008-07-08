# test_parse.py

# tests correction of source lines parcing

from __future__ import with_statement
import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_line import *

class ParserTestCase(unittest.TestCase):
  def testEmptyLines(self):
    empties = \
"""\t
\t\t
\t \t
                
  \t
*
* 
* \t ab abc
* *
*+*""".split("\n")

    for line in empties:
      self.assertEqual(parse_line(line), None)
    
    bad_empties = \
""" * bad comment
  * * bad comment""".split("\n")

    for line in bad_empties:
      self.assertRaises(AssemblySyntaxError, parse_line, line)

  def testLabels(self):
    def lines(labels):
      return [ (l + ' nop', l) for l in labels.split(' ') ]
    
    correct_labels = 'blah a z 123y321 1a1 a1 1a 123456789a'

    for l,label in lines(correct_labels):
      line = parse_line(l)

      self.assertEqual(line.label, label.upper())

    incorrect_labels = '123 1 2 label* # %'

    for l,_ in lines(incorrect_labels):
      self.assertRaises(InvalidLabelError, parse_line, l)

    self.assertRaises(TooLongLabelError, parse_line, 'VERYLONGLABEL NOP')

  def testFullLines(self):
    self.checkLine(parse_line('label nop'),                   'LABEL', 'NOP', None)
    self.checkLine(parse_line(' nop'),                        None, 'NOP', None)
    self.checkLine(parse_line("\tnop"),                       None, 'NOP', None)
    self.checkLine(parse_line("\tnop op"),                    None, 'NOP', 'OP')
    self.checkLine(parse_line("\tnop op comment"),            None, 'NOP', 'OP')
    self.checkLine(parse_line("label nop op comment"),        'LABEL', 'NOP', 'OP')
    self.checkLine(parse_line("label\tmove\t123\t* comment"), 'LABEL', 'MOVE', '123')

    self.assertRaises(MissingMnemonicError, parse_line, "labelonly")
    self.assertRaises(UnknownMnemonicError, parse_line, "label qqq")
    self.assertRaises(UnknownMnemonicError, parse_line, "\tqqq")
    self.assertRaises(UnknownMnemonicError, parse_line, "\tqqq op")
    self.assertRaises(UnknownMnemonicError, parse_line, " mov op comment")

  def checkLine(self, line, label, mnemonic, operand):
    self.assertEqual( (line.label, line.mnemonic, line.operand), (label, mnemonic, operand) )

suite = unittest.makeSuite(ParserTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
