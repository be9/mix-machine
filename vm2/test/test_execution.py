import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from execution import *
from errors import *

class ExecutionTestCase(unittest.TestCase):
  def blahTestFinder(self):
    array = [0, 10, 20, 25]
    tests = [
      (0, (0, True)),
      (25, (25, True)),
      (10, (10, True)),
      (5, (0, False)),
      (9, (0, False)),
      (15, (10, False)),
      (26, (25, False)),
    ]
    for value, result in tests:
      self.assertEqual(find_nearest_down(array, value), result)

suite = unittest.makeSuite(ExecutionTestCase, 'test')

if __name__ == "__main__":
  unittest.main()
