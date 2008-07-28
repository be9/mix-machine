# test_parse_lines.py

# tests correctness of source lines parsing

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'assembler'))
from parse_line import *
from errors import *

class ParserLinesTestCase(unittest.TestCase):
  def check(self, code, lines, expected_errors = []):
    result, errors = parse_lines(code.split("\n"))

    self.assertEqual(result, lines)
    self.assertEqual(errors, expected_errors)

  def testNoErrors(self):
    self.check(" nop\n end 0", 
      [
        Line(None, "NOP", None, 1),
        Line(None, "END", "0",  2),
      ])

    self.check("""\
STart eNTA 3 this is start of my mega program
LABEL1 \tStA LABEL1 sample of self modified code
* i love this program

* empty lines


\toRIg 1000
 equ 18 device
9H hlt
 eND 0
 and this is my
 long
 long poem""",
      [
        Line("START", "ENTA", "3", 1),
        Line("LABEL1", "STA", "LABEL1", 2),
        Line(None, "ORIG", "1000", 8),
        Line(None, "EQU", "18", 9),
        Line("9H", "HLT", None, 10),
        Line(None, "END", "0", 11),
      ])

  def testErrors(self):
    self.check("""\
 nopp
 sta 5
LABELLONG44 enta 5
\t* end 0""",
      [
        Line(None, "STA", "5", 2),
      ],
      [
        (1, UnknownOperationError("NOPP")),
        (3, TooLongLabelError("LABELLONG44")),
        (4, UnknownOperationError("*")),
        (4, NoEndError())
      ])

    self.check("""\
 nopp
 sta 5
LABELLONG44 enta 5""",
      [
        Line(None, "STA", "5", 2),
      ],
      [
        (1, UnknownOperationError("NOPP")),
        (3, TooLongLabelError("LABELLONG44")),
        (3, NoEndError())
      ])
    
    self.check("""\
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
 eND 0""",
      [
        Line("START", "ENTA", "3", 1),
        Line("LABEL1", "STA", "LABEL1", 2),
        Line(None, "EQU", "18", 11),
        Line(None, "END", "0", 15),
      ],
      [
        (3, MissingOperationError()),
        (8, InvalidLabelError("4353")),
        (9, InvalidLabelError("LABEL%")),
        (10, UnknownOperationError("ORIGG")),
        (12, UnknownOperationError("*HLT")),
        (13, UnknownOperationError("*")),
        (14, TooLongLabelError("AAAAAAAAAAAA"))
      ])
    
suite = unittest.makeSuite(ParserLinesTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
