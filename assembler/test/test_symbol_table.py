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
        Line("PRINTER","EQU","18",1),
        Line("NULL","ORIG","PRINTER",2),
        Line("START","ENTA","4",3),
        Line(None,"NOP",None,4),
        Line(None,"END","START",5)
      ],
      {"NULL" : 0, "START" : 18, "PRINTER" : 18}
    )

    # test locals
    self.check(
      [
        Line("PRINTER","EQU","18",1),
        Line("NULL","ORIG","PRINTER",2),
        Line("START","ENTA","4",3),
        Line("9H","EQU","547",4),
        Line(None,"ORIG","9B",5),
        Line("TESTLABEL","NOP",None,6),
        Line(None,"ORIG","TESTLABEL",7),
        Line("TESTLABEL3","NOP",None,8),
        Line("9H","EQU","745",9),
        Line(None,"ORIG","9B",10),
        Line("TESTLABEL2","NOP",None,11),
        Line(None,"END","START",12)
      ],
      {
        "NULL" : 0,
        "START" : 18,
        "PRINTER" : 18,
        "TESTLABEL" : 547,
        "TESTLABEL2" : 745,
        "TESTLABEL3" : 547
      },
      {
        "9H" : [(547, 4), (745, 9)]
      }
    )

    self.check(
      [
        Line("PRINTER666",  "EQU",  "18",         1),
        Line("0LABEL",      "CON",  "19",         2),
        Line("1LABEL",      "ALF",  "HELLO",      3),
        Line("9L",          "ORIG", "0LABEL",     4),
        Line("9H",          "NOP",  None,         5),
        Line("123456789L",  "NOP",  None,         6),
        Line("0H",          "ENTA", "9B",         7),
        Line(None,          "ORIG", "100",        8),
        Line("9H",          "HLT",  None,         9),
        Line(None,          "END",  "1000",       10),
      ],
      {
        "PRINTER666" : 18,
        "0LABEL" : 0,
        "1LABEL" : 1,
        "9L" : 2,
        "123456789L" : 1
      },
      {
        "0H" : [(2, 7)],
        "9H" : [(0, 5), (100, 9)]
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
        Line(None,          "ORIG", "3B",         8),
        Line(None,          "ORIG", "UNKNWN",     9),
        Line(None,          "ORIG", "18%",        10),
        Line("9H",          "HLT",  None,         11),
        Line(None,          "END",  "1000",       12),
      ],
      {
        "PRINTER666" : 18,
        "OLABEL" : 0,
        "9L" : 2,
        "123456789L" : 1
      },
      {
        "0H" : [(1002, 7)],
        "9H" : [(1000, 5), (1003, 11)]
      },
      [
        (6, RepeatedLabelError("123456789L")),
        (8, InvalidLocalLabelError("3B")),
        (9, InvalidExpressionError("UNKNWN")),
        (10, InvalidExpressionError("18%"))
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
