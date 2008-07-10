# all.py

# run all tests

import unittest
import test_parse_line
import test_parse_lines
import test_label_table

def suite():
  return unittest.TestSuite((test_parse_line.suite, test_parse_lines.suite, test_label_table.suite))

unittest.TextTestRunner().run(suite())
