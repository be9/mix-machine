import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from vm_command_parser import *
from vm_context import VMContext
from vm_word	import Word

class ParsedCommandTestCase(unittest.TestCase):
	def setUp(self):
		pass
	
	def testConstructor(self):
		pass
	
	def testWParts(self):
		w = Word([-1,2,3,4,5,6])
		com = ParsedCommand(w, None)
		
		self.assertEqual(com.w_addr(), w.int((0,2)))
		self.assertEqual(com.w_index(), w.int((3,3)))
		self.assertEqual(com.w_fmt(), w.int((4,4)))
		self.assertEqual(com.w_code(), w.int((5,5)))

	def testI(self):
		self.assertEqual(ParsedCommand( Word([1,0,0, 0 ,0,0]), None ).I(), 0)
		self.assertEqual(ParsedCommand( Word([1,0,0, 1 ,0,0]), None ).I(), 1)
		self.assertEqual(ParsedCommand( Word([1,0,0, 6 ,0,0]), None ).I(), 6)
		
		self.assertRaises(CommandInvalidIndexError, ParsedCommand( Word([1,0,0, 7 ,0,0]), None ).I)
		
	def testM(self):
		con = VMContext()
		
		con.rI[1] = Word(0)
		con.rI[2] = Word(2)
		con.rI[3] = Word(3)
		con.rI[4] = Word(4)
		con.rI[5] = Word(5)
		con.rI[6] = Word(-6)
		
		self.assertEqual(ParsedCommand( Word([1,1,1, 0, 0,0]), con ).M(), Word([1,1,1,0,0,0]).int((0,2)) )
		self.assertEqual(ParsedCommand( Word([-1,1,1, 0, 0,0]), con ).M(), Word([-1,1,1,0,0,0]).int((0,2)) )
		self.assertEqual(ParsedCommand( Word([1,1,1, 1, 0,0]), con ).M(), Word([1,1,1,0,0,0]).int((0,2)) )
		self.assertEqual(ParsedCommand( Word([-1,1,1, 1, 0,0]), con ).M(), Word([-1,1,1,0,0,0]).int((0,2)) )
		self.assertEqual(ParsedCommand( Word([1,1,1, 5, 0,0]), con ).M(), Word([1,1,1,0,0,0]).int((0,2)) + 5 )
		self.assertEqual(ParsedCommand( Word([-1,1,1, 5, 0,0]), con ).M(), Word([-1,1,1,0,0,0]).int((0,2)) + 5)
		self.assertEqual(ParsedCommand( Word([1,1,1, 6, 0,0]), con ).M(), Word([1,1,1,0,0,0]).int((0,2)) - 6 )
		self.assertEqual(ParsedCommand( Word([-1,1,1, 6, 0,0]), con ).M(), Word([-1,1,1,0,0,0]).int((0,2)) -6 )
		
		self.assertRaises(CommandInvalidIndexError, ParsedCommand( Word([1,0,0, 7 ,0,0]), con ).M)

	def testF(self):
		self.assertEqual(ParsedCommand( Word([1,0,0,0, 0*8 + 0 ,0]), None ).F(), (0,0))
		self.assertEqual(ParsedCommand( Word([1,0,0,0, 0*8 + 5 ,0]), None ).F(), (0,5))
		self.assertEqual(ParsedCommand( Word([1,0,0,0, 5*8 + 5 ,0]), None ).F(), (5,5))
		self.assertEqual(ParsedCommand( Word([1,0,0,0, 2*8 + 3 ,0]), None ).F(), (2,3))
		
		self.assertRaises(CommandInvalidFormatError, ParsedCommand( Word([1,0,0,0, 0*8 + 7 ,0]), None ).F)
		self.assertRaises(CommandInvalidFormatError, ParsedCommand( Word([1,0,0,0, 7*8 + 0 ,0]), None ).F)
		self.assertRaises(CommandInvalidFormatError, ParsedCommand( Word([1,0,0,0, 3*8 + 2 ,0]), None ).F)
		
suite = unittest.makeSuite(ParsedCommandTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
