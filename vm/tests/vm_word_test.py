import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from vm_word import *

class WordTestCase(unittest.TestCase):
	def setUp(self):
		pass
	
	def testConstructor(self):
		inits_ok = [	# bytes initializer
				([1, 0,0,0,0,0], [1,0,0,0,0,0]),
				([-1, 0,0,0,0,0], [-1,0,0,0,0,0]),
				([1, 1,1,1,1,1], [1,1,1,1,1,1]),
				([1, MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE], [1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE]),
				
				# integer initializer
				(0, [1,0,0,0,0,0]),
				(-100, [-1,0,0,0,1,36]),
				(MAX_WORD, [1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE]),
				(-MAX_WORD, [-1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE]),
				
				# float initializer
				# string initializer
			]
				
		for i in inits_ok:
			self.assertEqual(Word(i[0])._Word__val, i[1])
		
		inits_bad = [	# bytes initializer
				([], WordError), ([1], WordError), ([1,1,1,1,1,1,1], WordError),	# invalid bytes len
				([0, 1,1,1,1,1], WordError),	([2, 1,1,1,1,1], WordError),		# invalid sign byte
				([1, -1,1,1,1,1], WordError), ([1, MAX_BYTE+10,1,1,1,1], WordError),	# byte value out of range
				([1, 1,1,1,1,-1], WordError), ([1, 1,1,1,1,MAX_BYTE+10], WordError),
				([1.0, 1.0, 1.0, 1.0, 1.0], WordError),					# invalid byte type
				
				# integer initializer
				(MAX_WORD+10, WordError),	# word value out of range
				(-MAX_WORD-10, WordError),
				
				# float initializer
				# string initializer
				
				# unknown type initializer
				({"unknown": "type"}, WordError)
			]
				
		for i in inits_bad:
			self.assertRaises(i[1], Word, i[0])

	def testSetBytes(self):
		w = Word([1, 10, 20, 30, 40, 50])
		ops_ok = [	([-1, 11,12,13,14,15], 	(0,5), [-1, 11,12,13,14,15]),
				([-1], 			(0,0), [-1, 10, 20, 30, 40, 50]),
				([11,12,13,14,15], 	(1,5), [1, 11,12,13,14,15]),
				([13,14], 		(3,4), [1, 10, 20, 13, 14, 50]),
				([13], 			(3,3), [1, 10, 20, 13, 40, 50])
			]
			
		for i in ops_ok:
			w = Word([1, 10, 20, 30, 40, 50])
			self.assertEqual(w.set_bytes(i[0], i[1])._Word__val, i[2])
			
		ops_bad = [	# invalid format
				([1, 11,12,13,14,15], (-1,5), WordError),
				([1, 11,12,13,14,15], (1,6), WordError),
				([1, 11,12,13,14,15], (3,1), WordError),
				
				# format mismatch
				([1, 11,12,13,14,15], 	(2,3), WordError),
				([], 	(0,5), WordError),
				([1], 	(0,5), WordError),
				
				# invalid sign byte
				([0, 11,12,13,14,15], 	(0,5), WordError),
				([-2, 11,12,13,14,15], 	(0,5), WordError),
				
				# bytes out of range
				([1, -1,1,1,1,1],		(0,5), WordError),
				([1, MAX_BYTE+10,1,1,1,1],	(0,5), WordError),
				([1, 1,1,1,1,-1],		(0,5), WordError),
				([1, 1,1,1,1,MAX_BYTE+10],	(0,5), WordError)
			]
			
		for i in ops_bad:
			w = Word([1, 10, 20, 30, 40, 50])
			self.assertRaises(i[2], w.set_bytes, i[0], i[1])

	def testGetBytes(self):
		w = Word([-1, 11, 12, 13, 14, 15])
		ops_ok = [	((0,5), [-1, 11,12,13,14,15]),
				((0,0), [-1]),
				((1,5), [11,12,13,14,15]),
				((3,4), [13, 14]),
				((3,3), [13])
			]
			
		for i in ops_ok:
			self.assertEqual(w.get_bytes(i[0]), i[1])
			
		ops_bad = [	# invalid format
				((-1,5), WordError),
				((1,6), WordError),
				((3,1), WordError),
			]
			
		for i in ops_bad:
			self.assertRaises(i[1], w.set_bytes, i[0])


	def testCasts(self):
		pass

suite = unittest.makeSuite(WordTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
