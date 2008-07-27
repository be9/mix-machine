import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from vm_command import *

class CommandListTestCase(unittest.TestCase):
	def setUp(self):
		pass
	
	def testAdd(self):
		lst = CommandList()
		
		lst.add_command(1, -1, None, 0, "")
		lst.add_command(2, 0, None, 0,  "")
		
		self.assertEqual(lst.commands[(1,-1)], Command(1,-1,None,0,"",False))
		self.assertEqual(lst.commands[(2,0)], Command(2,0,None,0,"",False))
		
		self.assertRaises(CommandAlreadyExistError, lst.add_command, 1, -1, None, 0,  "")
		self.assertRaises(CommandAlreadyExistError, lst.add_command, 1, 0, None, 0,  "")
		self.assertRaises(CommandAlreadyExistError, lst.add_command, 2, 0, None, 0,  "")
		self.assertRaises(CommandAlreadyExistError, lst.add_command, 2, -1, None, 0,  "")
		
	def testGet(self):
		lst = CommandList()
		
		lst.add_command(1, -1, None, 0, "")
		lst.add_command(2, 0, None, 0,  "")
		
		self.assertEqual(lst.get_command(1,-1), Command(1,-1,None,0,"",False))
		self.assertEqual(lst.get_command(1,1), Command(1,-1,None,0,"",False))
		self.assertEqual(lst.get_command(1,2), Command(1,-1,None,0,"",False))
		
		self.assertEqual(lst.get_command(2,0), Command(2,0,None,0,"",False))
		
		self.assertRaises(CommandNotFoundError, lst.get_command, 2, -1)
		self.assertRaises(CommandNotFoundError, lst.get_command, 2, 1)
		
		self.assertRaises(CommandNotFoundError, lst.get_command, 3, -1)
		self.assertRaises(CommandNotFoundError, lst.get_command, 3, 0)
		
suite = unittest.makeSuite(CommandListTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
