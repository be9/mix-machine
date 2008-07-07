# test_parse.py

# tests correction of source lines parcing

from __future__ import with_statement
import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_line import *

class ParserTestCase(unittest.TestCase):
	def testEmptyLine(self):
		with open("test/empties.dat","r") as file:
			for line in file:
				self.assertEqual(parse_line(line), None)

	def testErrors(self):
		with open("test/errors.dat","r") as file:
			for line in file:
				self.assertRaises(AssemblySyntaxError, parse_line, line)

suite = unittest.makeSuite(ParserTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
