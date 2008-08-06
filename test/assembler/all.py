# all.py

# run all tests

import unittest
import test_parse_argument
import test_parse_line
import test_parse_lines
import test_symbol_table
import test_memory
import test_operations
import test_assemble
import test_complete_programs
import test_listing

def suite():
  return unittest.TestSuite((
    test_parse_line.suite,
    test_parse_lines.suite,
    test_symbol_table.suite,
    test_memory.suite,
    test_operations.suite,
    test_parse_argument.suite,
    test_assemble.suite,
    test_complete_programs.suite,
    test_listing.suite
  ))

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite())
