import unittest
import basetestcase

class VM3MathTestCase(basetestcase.VM3BaseTestCase):
  def testADD(self):
    self.check1(
      regs = {'A': [+1, 0, 0, 0, 0, 0]},
      memory = {0: [+1, 0, 0, 0, 5, 1]},
      diff = {'CA': 1, 'A': [+1, 0, 0, 0, 5, 1]},
      cycles = 2
    )

suite = unittest.makeSuite(VM3MathTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
