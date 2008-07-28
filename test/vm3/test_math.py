import unittest
from basetestcase import *

class VM3MathTestCase(VM3BaseTestCase):
  def testADD(self):
    self.check1(
      regs = {'A': [+1, 0, 0, 0, 0, 0]},
      memory = {0: [+1, 0, 0, 0, 5, 1]},
      diff = {'CA': 1, 'A': [+1, 0, 0, 0, 5, 1]},
      cycles = 2
    )

    self.check1(
      regs = {'A': [+1, 5, 4, 3, 2, 1]},
      memory = {0: [+1, 0, 0, 0, 5, 1]},
      diff = {'CA': 1, 'A': [+1, 5, 4, 3, 7, 2]},
      cycles = 2
    )

    self.check1(
      regs = {'A': [+1, 5, 4, 3, 2, 1]},
      memory = {0: [+1, 0, 0, 0,28, 1]}, # 28 = (3:4)
      diff = {'CA': 1, 'A': [+1, 5, 4, 3, 2, 29]},
      cycles = 2
    )

    self.check1(
      regs = {'A': [+1, 5, 4, 3, 2, 1]},
      memory = {0: [+1, 0, 0, 0, 2, 1]}, # 2 = (0:2)
      diff = {'CA': 1},
      cycles = 2,
      message = "adding zero-part of word"
    )

    self.check1(
      regs = {'A': [-1, 63, 2, 0, 0, 3]},
      memory = {
        0  : [+1, 63, 2, 0, 0, 3],
        10 : [+1, 0, 0, 0, 5, 1]
      },
      startadr = 10,
      diff = {'CA': 11, 'A': [-1, 0, 0, 0, 0, 0]},
      cycles = 2,
      message = "saving sign of rA, if rA == 0"
    )

    self.check1(
      regs = {'A': [+1, 63, 2, 0, 0, 3]},
      memory = {
        0  : [-1, 63, 2, 0, 0, 3],
        10 : [+1, 0, 0, 0, 5, 1]
      },
      startadr = 10,
      diff = {'CA': 11, 'A': [+1, 0, 0, 0, 0, 0]},
      cycles = 2,
      message = "saving sign of rA, if rA == 0"
    )

    self.check1(
      regs = {'A': [+1, 63, 60, 60, 60, 60]},
      memory = {
        0  : [+1, 2, 3, 2, 1, 4],
        10 : [+1, 0, 0, 0, 5, 1]
      },
      startadr = 10,
      diff = {'CA': 11, 'OF' : 1, 'A': [+1, 1, 63, 62, 62, 0]},
      cycles = 2,
      message = "overflow test"
    )

    self.check1(
      regs = {'A': [-1, 63, 60, 60, 60, 60]},
      memory = {
        0  : [-1, 2, 3, 2, 1, 4],
        10 : [+1, 0, 0, 0, 5, 1]
      },
      startadr = 10,
      diff = {'CA': 11, 'OF' : 1, 'A': [-1, 1, 63, 62, 62, 0]},
      cycles = 2,
      message = "negative overflow test"
    )



    self.assertRaises(InvalidFieldSpec, self.check1,
      regs = {'A': [+1, 5, 4, 3, 2, 1]},
      memory = {0: [+1, 0, 0, 0,26, 1]}, # 26 = (3:2)
      diff = {'CA': 1, 'A': [+1, 5, 4, 3, 2, 29]},
      cycles = 2
    )

    self.assertRaises(InvalidAddress, self.check1,
      regs = {'A': [-1, 63, 60, 60, 60, 60]},
      memory = {
        0  : [-1, 2, 3, 2, 1, 4],
        10 : [-1, 0, 1, 0, 5, 1]
      },
      startadr = 10,
      diff = {'CA': 11, 'OF' : 1, 'A': [-1, 1, 63, 62, 62, 0]},
      cycles = 2
    )

    self.assertRaises(InvalidIndex, self.check1,
      regs = {'A': [-1, 63, 60, 60, 60, 60]},
      memory = {
        0  : [-1, 2, 3, 2, 1, 4],
        10 : [+1, 63, 1, 8, 5, 1]
      },
      startadr = 10,
      diff = {'CA': 11, 'OF' : 1, 'A': [-1, 1, 63, 62, 62, 0]},
      cycles = 2
    )

suite = unittest.makeSuite(VM3MathTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
