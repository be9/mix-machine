# test_symbol_table.py

# testing of module label_table

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_line import Line
from symbol_table import *

class LabelsTestCase(unittest.TestCase):
  def check(self, lines, expected_labels, expected_local_labels = {}, expected_errors = []):
    labels, local_labels, errors = create_symbol_table(lines)
    self.assertEqual(labels, expected_labels)
    self.assertEqual(local_labels, expected_local_labels)
    self.assertEqual(errors, expected_errors)

  def testNoErrors(self):
    self.check(
      [
        Line("NULL","ORIG","3000",1),
        Line("START","ENTA","4",2),
        Line(None,"NOP",None,3),
        Line(None,"END","START",4)
      ],
      {"NULL" : 0, "START" : 3000}
    )

    self.check(
      [
        Line("PRINTER666",  "EQU",  "18",         1),
        Line("OLABEL",      "CON",  "19",         2),
        Line("1LABEL",      "ALF",  "HELLO",      3),
        Line("9L",          "ORIG", "1000",       4),
        Line("9H",          "NOP",  None,         5),
        Line("123456789L",  "NOP",  None,         6),
        Line("0H",          "ENTA", "PRINTER666", 7),
        Line(None,          "ORIG", "100",        8),
        Line("9H",          "HLT",  None,         9),
        Line(None,          "END",  "1000",       10),
      ],
      {
        "PRINTER666" : 18,
        "OLABEL" : 0,
        "1LABEL" : 1,
        "9L" : 2,
        "123456789L" : 1001
      },
      {
        "0H" : [(1002, 7)],
        "9H" : [(1000, 5), (100, 9)]
      }
    )

  def testErrors(self):
    self.check(
      [
        Line("NULL","ORIG","3000",1),
        Line("START","ENTA","4",2),
        Line("START","NOP",None,3),
        Line(None, "ORIG", "5000", 4),
        Line(None,"END","START",5)
      ],
      {"NULL" : 0, "START" : 3000},
      {},
      [
        (3, RepeatedLabelError("START")),
        (4, LineNumberError(5000))
      ]
    )

    self.check(
      [
        Line("PRINTER666",  "EQU",  "18",         1),
        Line("OLABEL",      "CON",  "19",         2),
        Line("123456789L",  "ALF",  "HELLO",      3),
        Line("9L",          "ORIG", "1000",       4),
        Line("9H",          "NOP",  None,         5),
        Line("123456789L",  "NOP",  None,         6),
        Line("0H",          "ENTA", "PRINTER666", 7),
        Line(None,          "ORIG", "100",        8),
        Line("9H",          "HLT",  None,         9),
        Line(None,          "END",  "1000",       10),
      ],
      {
        "PRINTER666" : 18,
        "OLABEL" : 0,
        "9L" : 2,
        "123456789L" : 1
      },
      {
        "0H" : [(1002, 7)],
        "9H" : [(1000, 5), (100, 9)]
      },
      [ (6, RepeatedLabelError("123456789L")) ]
    )

    self.check(
      [
        Line("PRINTER666",  "EQU",  "18",         1),
        Line("OLABEL",      "CON",  "19",         2),
        Line("123456789L",  "ALF",  "HELLO",      3),
        Line("9L",          "ORIG", "1000",       4),
        Line("9H",          "NOP",  None,         5),
        Line("123456789L",  "NOP",  None,         6),
        Line("0H",          "ENTA", "PRINTER666", 7),
        Line(None,          "ORIG", "3998",       8),
        Line("9H",          "NOP",  None,         9),
        Line(None,          "NOP",  None,         10),
        Line(None,          "NOP",  None,         11),
        Line("4001LABEL",   "NOP",  None,         12),
        Line(None,          "END",  "1000",       13),
      ],
      {
        "PRINTER666" : 18,
        "OLABEL" : 0,
        "9L" : 2,
        "123456789L" : 1,
        "4001LABEL" : 4001
      },
      {
        "0H" : [(1002, 7)],
        "9H" : [(1000, 5), (3998, 9)]
      },
      [
        (6, RepeatedLabelError("123456789L")),
        (11, LineNumberError(4000)),
        (12, LineNumberError(4001))
      ]
    )

suite = unittest.makeSuite(LabelsTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
