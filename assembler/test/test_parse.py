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
    def lines(labels):
      return [ (l + ' nop', l) for l in labels.split(' ') ]
    
    correct_labels = 'blah a z 123y321 1a1 a1 1a 123456789a'

    for l,label in lines(correct_labels):
      line = parse_line(l)

      self.assertEqual(line.label, label.upper())

    incorrect_labels = '123 1 2 a123456789aa'

    for l,_ in lines(incorrect_labels):
      self.assertRaises(AssemblySyntaxError, parse_line, l)

suite = unittest.makeSuite(ParserTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
