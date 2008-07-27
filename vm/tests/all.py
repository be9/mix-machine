import unittest

import vm_command_test
import vm_command_parser_test
import vm_memory_test
import vm_word_test

def suite():
  return unittest.TestSuite(
    (
	vm_command_test.suite,
	vm_command_parser_test.suite,
	vm_memory_test.suite,
	vm_word_test.suite
    )
  )

unittest.TextTestRunner().run(suite())