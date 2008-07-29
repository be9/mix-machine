import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'vm'))
from vm_word_math import *
from vm_word import *

class WordMathTestCase(unittest.TestCase):
    def setUp(self):
	    pass
	
    def testAdd(self):
        ops = [ ([1,0,0,0,0,0], [1,0,0,0,0,0], [1,0,0,0,0,0], 0),
                ([-1,0,0,0,0,0], [-1,0,0,0,0,0], [-1,0,0,0,0,0], 0),
                ([-1,0,0,0,0,0], [1,0,0,0,0,0], [-1,0,0,0,0,0], 0),
                ([1,0,0,0,0,0], [-1,0,0,0,0,0], [1,0,0,0,0,0], 0),
                
                ([1,1,2,3,4,5], [1,1,2,3,4,5], [1,2,4,6,8,10], 0),
                ([-1,1,2,3,4,5], [1,1,2,3,4,5], [-1,0,0,0,0,0], 0),
                ([1,1,2,3,4,5], [-1,1,2,3,4,5], [1,0,0,0,0,0], 0),
                
                ([1,1,2,3,4,5], [1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE], [1,1,2,3,4,4], 1),
                ([-1,1,2,3,4,5], [-1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE], [-1,1,2,3,4,4], 1),

                ([1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE], [1,0,0,0,0,1], [1,0,0,0,0,0], 1),
                ([-1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE], [-1,0,0,0,0,1], [-1,0,0,0,0,0], 1)
                ]

        for op1, op2, res, ov in ops:
            a = Add(Word(op1), Word(op2))
            self.assertEqual(a.res.get_bytes(), res)
            self.assertEqual(a.ov, ov)

    def testSub(self):
        ops = [ ([1,0,0,0,0,0], [1,0,0,0,0,0], [1,0,0,0,0,0], 0),
                ([-1,0,0,0,0,0], [-1,0,0,0,0,0], [-1,0,0,0,0,0], 0),
                ([-1,0,0,0,0,0], [1,0,0,0,0,0], [-1,0,0,0,0,0], 0),
                ([1,0,0,0,0,0], [-1,0,0,0,0,0], [1,0,0,0,0,0], 0),
                
                ([1,1,2,3,4,5], [-1,1,2,3,4,5], [1,2,4,6,8,10], 0),
                ([1,1,2,3,4,5], [1,1,2,3,4,5], [1,0,0,0,0,0], 0),
                ([-1,1,2,3,4,5], [-1,1,2,3,4,5], [-1,0,0,0,0,0], 0),
                
                ([1,1,2,3,4,5], [-1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE], [1,1,2,3,4,4], 1),
                ([-1,1,2,3,4,5], [1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE], [-1,1,2,3,4,4], 1),

                ([1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE], [-1,0,0,0,0,1], [1,0,0,0,0,0], 1),
                ([-1,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE,MAX_BYTE], [1,0,0,0,0,1], [-1,0,0,0,0,0], 1)
                ]

        for op1, op2, res, ov in ops:
            a = Sub(Word(op1), Word(op2))
            self.assertEqual(a.res.get_bytes(), res)
            self.assertEqual(a.ov, ov)

suite = unittest.makeSuite(WordMathTestCase, 'test')

if __name__ == "__main__":
    unittest.main()
