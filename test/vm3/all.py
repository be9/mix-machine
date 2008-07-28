import unittest
import test_math

def suite():
  return unittest.TestSuite(
    (
      test_math.suite,
    )
  )
