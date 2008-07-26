import unittest
import test_read_memory
import test_virt_machine
import test_execution
import test_word

def suite():
  return unittest.TestSuite(
    (
      test_read_memory.suite,
      test_virt_machine.suite,
      test_execution.suite,
      test_word.suite
    )
  )

unittest.TextTestRunner().run(suite())