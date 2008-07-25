import unittest
import test_read_memory
import test_virt_machine

def suite():
  return unittest.TestSuite(
    (
      test_read_memory.suite,
      test_virt_machine.suite
    )
  )

unittest.TextTestRunner().run(suite())