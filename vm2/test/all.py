import unittest
import test_read_memory
import test_virt_machine
import test_execution

def suite():
  return unittest.TestSuite(
    (
      test_read_memory.suite,
      test_virt_machine.suite,
      test_execution.suite,
    )
  )

unittest.TextTestRunner().run(suite())