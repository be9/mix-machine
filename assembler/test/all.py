# all.py

# run all tests

import unittest
import test_parse_argument
import test_parse_line
import test_parse_lines
import test_symbol_table
import test_memory
import test_operations

def suite():
  return unittest.TestSuite((test_parse_line.suite, test_parse_lines.suite, test_symbol_table.suite, \
    test_memory.suite, test_operations.suite, test_parse_argument.suite))

unittest.TextTestRunner().run(suite())
