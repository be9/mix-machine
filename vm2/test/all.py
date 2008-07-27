import unittest
import test_read_memory
import test_virt_machine
import test_execution
import test_word
import test_word_parser
import test_vm3

def suite():
  return unittest.TestSuite(
    (
      test_read_memory.suite,
      test_virt_machine.suite,
      test_execution.suite,
      test_word.suite,
      test_word_parser.suite,
      test_vm3.suite
    )
  )

unittest.TextTestRunner().run(suite())