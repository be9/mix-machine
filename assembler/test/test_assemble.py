# test_assemble.py

# testing of assemle module

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_line import *
from assemble import *
from memory import *

class AssembleTestCase(unittest.TestCase):
  def check(self, lines, labels, local_labels, memory_part, start_address, errors):
    symbol_table = SymbolTable(None, labels, local_labels)
    result = assemble(lines, symbol_table)
    self.assertTrue(result[0].cmp_memory(memory_part))
    self.assertEqual(result[1], start_address)
    self.assertEqual(result[2], errors)

  def testNoErrors(self):
    self.check(
      lines = [
        Line(None,         "ORIG", "30",   1),
        Line("7H",         "ENTA", "15",   2),
        Line(None,         "ENN2", "TEMP", 3),
        Line("TEMP",       "EQU",  "-2",   4),
        Line(None,         "HLT",  "64",   5),
        Line(None,         "END",  "7B",   6)
      ],
      labels = {
        "TEMP": -2
      },
      local_labels = {
        "7H": [(30, 2)]
      },
      memory_part = {
        30: [+1, 00, 15, 00, 02, 48],
        31: [-1, 00, 02, 00, 03, 50],
        32: [+1, 01, 00, 00, 02, 05]
      },
      start_address = 30,
      errors = []
    )

suite = unittest.makeSuite(AssembleTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
