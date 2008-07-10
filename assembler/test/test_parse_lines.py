# test_parse_lines.py

# tests correction of source lines parcing

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_lines import *
from parse_line import *
from errors import *

class ParserLinesTestCase(unittest.TestCase):
  def checkLine(self, line1, line2):
    self.assertEqual(line1.label, line2.label)
    self.assertEqual(line1.operation, line2.operation)
    self.assertEqual(line1.argument, line2.argument)
    self.assertEqual(line1.line_number, line2.line_number)

  def checkLines(self, lines1, lines2):
    self.assertEqual(len(lines1), len(lines2))
    for i in xrange(len(lines1)):
      self.checkLine(lines1[i], lines2[i])

  def checkErrors(self, errors1, errors2):
    self.assertEqual(len(errors1), len(errors2))
    for i in xrange(len(errors1)):
      self.assertEqual(errors1[i][0], errors2[i][0]) # check line number
      self.assertEqual(type(errors1[i][1]), type(errors2[i][1])) # check error messages types
      self.assertEqual(errors1[i][1].info, errors2[i][1].info) # check error message


  def testNoErrors(self):
    test = list()
    result = list()


    test.append("""\
 nop
 end 0""".split('\n'))

    result.append((
    [
    Line(None, "NOP", None, 1),
    Line(None, "END", "0", 2),
    ]
    , []
    ))


    test.append("""\
STart eNTA 3 this is start of my mega program
LABEL1 \tStA LABEL1 sample of self modified code
* i love this program

* empty lines


\toRIg 1000
 equ 18 device
9H hlt
 eND 0""".split('\n'))

    result.append((
    [
    Line("START", "ENTA", "3", 1),
    Line("LABEL1", "STA", "LABEL1", 2),
    Line(None, "ORIG", "1000", 8),
    Line(None, "EQU", "18", 9),
    Line("9H", "HLT", None, 10),
    Line(None, "END", "0", 11),
    ]
    , []
    ))

    for i in xrange( min(len(test),len(result)) ):
      parced = parse_lines(test[i])
      self.checkLines(parced[0], result[i][0]) # check result lines
      self.checkErrors(parced[1], result[i][1]) # check errors

  def testErrors(self):
    test = list()
    result = list()


    test.append("""\
 nopp
 sta 5
LABELLONG44 enta 5
\t* end 0""".split('\n'))

    result.append((
    [
    Line(None, "STA", "5", 2),
    ]
    , [
    (1, UnknownOperationError("NOPP")),
    (3, TooLongLabelError("LABELLONG44")),
    (4, UnknownOperationError("*"))
    ]
    ))


    test.append("""\
STart eNTA 3 this is start of my mega program
LABEL1 \tStA LABEL1 sample of self modified code
coolLabel\t\t
* i love this program

* empty lines

4353\tSTA\t0
label% nop 0
\toRIgg 1000
 equ 18 device
9H\t*hlt
 * sorry my A sometimes sticking
AAAAAAAAAAAA NOP
 eND 0""".split('\n'))

    result.append((
    [
    Line("START", "ENTA", "3", 1),
    Line("LABEL1", "STA", "LABEL1", 2),
    Line(None, "EQU", "18", 11),
    Line(None, "END", "0", 15),
    ]
    , [
    (3, MissingOperationError()),
    (8, InvalidLabelError("4353")),
    (9, InvalidLabelError("LABEL%")),
    (10, UnknownOperationError("ORIGG")),
    (12, UnknownOperationError("*HLT")),
    (13, UnknownOperationError("*")),
    (14, TooLongLabelError("AAAAAAAAAAAA"))
    ]
    ))

    for i in xrange( min(len(test),len(result)) ):
      parced = parse_lines(test[i])
      self.checkLines(parced[0], result[i][0]) # check result lines
      self.checkErrors(parced[1], result[i][1]) # check errors


suite = unittest.makeSuite(ParserLinesTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
