# test_parse.py

# tests correction of source lines parcing

from __future__ import with_statement
import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_line import *

empties = """
\t
\t\t
\t \t
                
  \t
*
* 
* \t ab abc
* *
*+*""".split("\n")

errors = \
"""	ENTU	100 comment
label	EQUU	5
 * bad comment
	* * bad comment
VERYLONGLABEL ENTA	5
6546	ENTA	3
label*	ENTA	3
%	ENTA	3
#	ENTA	3
label	EQUUUU""".split("\n")

class ParserTestCase(unittest.TestCase):
  def testEmptyLine(self):
    for line in empties:
      self.assertEqual(parse_line(line), None)

  def testErrors(self):
    for line in errors:
      self.assertRaises(AssemblySyntaxError, parse_line, line)

  def testLabels(self):
    correct_labels = 'blah a z 123y321 1a1 a1 1a 123456789a'.split(' ')

    for label in correct_labels:
      line = parse_line(label + ' nop')

      self.assertEqual(line.label, label.upper())

    incorrect_labels = '123 1 2 a123456789aa'.split(' ')

    for label in incorrect_labels:
      self.assertRaises(AssemblySyntaxError, parse_line, label + ' nop')

suite = unittest.makeSuite(ParserTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
