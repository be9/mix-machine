# test_parse_line.py

# tests correction of source lines parcing

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_line import *
from errors import *

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
\t* bad comment
\t\tbad comment
  * * bad comment""".split("\n")

    for line in bad_empties:
      self.assertRaises(AssemblySyntaxError, parse_line, line)

  def testLabels(self):

    # auxillary function
    def lines(labels):
      return [ (l + ' nop', l) for l in labels.split(' ') ]
    
    correct_labels = 'blah a z 123y321 1a1 a1 1a 123456789a 9H 9B 9F labellabel'

    # l - source line, label - label of this line
    for src_line,label in lines(correct_labels):
      self.assertEqual(parse_line(src_line).label, label.upper())

    incorrect_labels = '4F 4B 123 1 2 label* # % label,'

    for l,_ in lines(incorrect_labels):
      self.assertRaises(InvalidLabelError, parse_line, l)

    self.assertRaises(TooLongLabelError, parse_line, 'VERYLONGLABEL NOP')

  def testFullLines(self):
    self.checkLine(parse_line('label nop'),                   'LABEL', 'NOP', None)
    self.checkLine(parse_line('9f nop'),                      '9F', 'NOP', None)
    self.checkLine(parse_line(' nop'),                        None, 'NOP', None)
    self.checkLine(parse_line("\tnop"),                       None, 'NOP', None)
    self.checkLine(parse_line("\tnop arg"),                   None, 'NOP', 'ARG')
    self.checkLine(parse_line("\tnop arg comment"),           None, 'NOP', 'ARG')
    self.checkLine(parse_line("label nop arg comment"),       'LABEL', 'NOP', 'ARG')
    self.checkLine(parse_line("label\tmove\t123\t* comment"), 'LABEL', 'MOVE', '123')

    self.assertRaises(MissingOperationError, parse_line, "labelonly")
    self.assertRaises(UnknownOperationError, parse_line, "label $^%$")
    self.assertRaises(UnknownOperationError, parse_line, "label nopp")
    self.assertRaises(UnknownOperationError, parse_line, "\tqqq")
    self.assertRaises(UnknownOperationError, parse_line, "\tqq* arg")
    self.assertRaises(UnknownOperationError, parse_line, "\tqqq arg")
    self.assertRaises(UnknownOperationError, parse_line, " mov arg comment")

  def checkLine(self, line, label, operation, argument):
    self.assertEqual( (line.label, line.operation, line.argument), (label, operation, argument) )

suite = unittest.makeSuite(ParserTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
