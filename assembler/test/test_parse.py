import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse import parse

class ParserTestCase(unittest.TestCase):
  def testEmptyLine(self):
    for line in ('', ' ', '* abc', '*', "  \t\t  "):
      self.assertEqual(parse(line), None)

  def testLabel(self):
    self.assertEqual(parse('blah nop').label, 'blah')

suite = unittest.makeSuite(ParserTestCase, 'test')

if __name__ == "__main__":
  unittest.main()
