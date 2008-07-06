# test_parse.py

# tests correction of source lines parcing

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_line import *

empties = ("", " ", "\t", "\t\t", " \t \t", "*", "* ", "* \t ab abc")
errors = (" * a a a", " *", " label nop 1", "la#bel nop f", " nopp f")	

class ParserTestCase(unittest.TestCase):
	def testEmptyLine(self):
		for line in empties:
			self.assertEqual(parse_line(line), None)

	def testErrors(self):
		for line in errors:
			print "<",line,">"
			# this fails!!! :(
			self.assertRaises(AssemblySyntaxError, parse_line, line)
			
			# simply:
			#try:
			#	parse_line(line)
			#except AssemblySyntaxError:
			#	pass
			#else:
			#	self.fail("expected an AssemblySyntaxError")

suite = unittest.makeSuite(ParserTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
