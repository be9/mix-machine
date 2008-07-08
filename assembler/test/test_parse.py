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
*+*"""

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
label	EQUUUU"""

class ParserTestCase(unittest.TestCase):
  def testEmptyLine(self):
    for line in empties.split("\n"):
      self.assertEqual(parse_line(line), None)

  def testErrors(self):
    for line in errors.split("\n"):
      self.assertRaises(AssemblySyntaxError, parse_line, line)

suite = unittest.makeSuite(ParserTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
