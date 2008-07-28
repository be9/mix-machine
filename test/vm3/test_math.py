import unittest
import basetestcase

class VM3MathTestCase(basetestcase.VM3BaseTestCase):
  def testADD(self):
    self.assertEqual(self.exec1(regs={'A': [+1, 0, 0, 0, 0, 0]}, memory={0: [+1, 0, 0, 0, 0, 1]}),
        {'CA': 1, 'A': [+1, 0, 0, 0, 0, 1]})

suite = unittest.makeSuite(VM3MathTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
