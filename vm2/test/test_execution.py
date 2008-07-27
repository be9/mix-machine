import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from execution import *
from errors import *

class ExecutionTestCase(unittest.TestCase):
  pass

suite = unittest.makeSuite(ExecutionTestCase, 'test')

if __name__ == "__main__":
  unittest.main()
