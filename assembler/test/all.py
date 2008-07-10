# all.py

# run all tests

import unittest
import test_parse_line
import test_parse_lines

def suite():
  return unittest.TestSuite((test_parse_line.suite, test_parse_lines.suite))

unittest.TextTestRunner().run(suite())
