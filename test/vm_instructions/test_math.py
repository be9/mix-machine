import unittest
from basetestcase import *

class VMMathTestCase(VMBaseTestCase):
  """ADDandSUB, MUL, DIV"""
  def testDIV(self):
    self.check1(
      regs = {
        'A': [-1, 0, 0, 0, 0, 0],
        'X': [+1,0, 0,0,0,0]
      },
      memory = {
        0  : [+1, 1, 2, 3, 4, 5],
        10 : [+1, 0, 0, 0,20, 4] # = (2:4)
      },
      startadr = 10,
      diff = {
        'CA': 11,
        'X': [-1, 0, 0, 0, 0, 0]
      },
      cycles = 12
    )
    self.check1(
      regs = {
        'A': [-1, 0, 0, 0, 18, 44],
        'X': [+1,11, 1,56,39,25]
      },
      memory = {
        0  : [+1, 1, 2, 3, 4, 5],
        10 : [+1, 0, 0, 0,20, 4] # = (2:4)
      },
      startadr = 10,
      diff = {
        'CA': 11,
        'A': [-1, 9, 8, 7, 6, 5],
        'X': [-1, 0, 0, 0, 0, 5]
      },
      cycles = 12
    )

    self.check1(
      regs = {
        'A': [-1, 0, 0, 0, 18, 44],
        'X': [+1,11, 1,56,39,25]
      },
      memory = {
        0  : [+1, 1, 2, 3, 4, 1],
        10 : [+1, 0, 0, 0,45, 4] # = (5:5)
      },
      startadr = 10,
      diff = {
        'OF':1,
        'CA': 11
      },
      cycles = 12,
      message = "overflow test"
    )

    self.check1(
      regs = {
        'A': [-1, 0, 0, 0, 18, 44],
        'X': [+1,11, 1,56,39,25]
      },
      memory = {
        0  : [+1, 1, 0, 3, 4, 1],
        10 : [+1, 0, 0, 0,18, 4] # = (2:2)
      },
      startadr = 10,
      diff = {
        'OF':1,
        'CA': 11
      },
      cycles = 12,
      message = "overflow test, divizion by zero"
    )

    self.assertRaises(InvalidIndex, self.exec1,
      memory = {
        0 : [+1, 63, 63, 44, 5, 4]
      }
    )
    self.assertRaises(InvalidAddress, self.exec1,
      regs = {"I6" : [+1, 0, 0, 0, 62, 31]},
      memory = {
        0 : [+1, 0, 1, 6, 5, 4]
      }
    )
    self.assertRaises(InvalidFieldSpec, self.exec1,
      memory = {
        0 : [+1, 2, 0, 0, 63, 4]
      }
    )


  def testMUL(self):
    self.check1(
      regs = {'A': [-1, 9, 8, 7, 6, 5]},
      memory = {
        0  : [+1, 1, 2, 3, 4, 5],
        10 : [+1, 0, 0, 0,20, 3] # = (2:4)
      },
      startadr = 10,
      diff = {
        'CA': 11,
        'A': [-1, 0, 0, 0, 18, 44],
        'X': [-1,11, 1,56,39,20]
      },
      cycles = 10
    )

    self.check1(
      regs = {'A': [+1, 9, 8, 7, 6, 5]},
      memory = {
        0  : [-1, 0, 0, 0, 0, 0],
        10 : [+1, 0, 0, 0, 5, 3]
      },
      startadr = 10,
      diff = {
        'CA': 11,
        'A': [-1, 0, 0, 0, 0, 0],
        'X': [-1, 0, 0, 0, 0, 0]
      },
      cycles = 10,
      message = "sign saving for multiplying by zero"
    )

    self.assertRaises(InvalidFieldSpec, self.exec1,
      memory = {
        10 : [+1, 0, 0, 0, 44, 3] # = (5:4)
      },
      startadr = 10,
    )
    self.assertRaises(InvalidAddress, self.exec1,
      memory = {
        10 : [+1, 63, 63, 0, 5, 3]
      },
      startadr = 10,
    )
    self.assertRaises(InvalidIndex, self.exec1,
      memory = {
        10 : [+1, 63, 63, 44, 5, 3]
      },
      startadr = 10,
    )


  def testADDandSUB(self):
    self.check1(
      regs = {'A': [+1, 0, 0, 0, 0, 0]},
      memory = {0: [+1, 0, 0, 0, 5, 1]},
      diff = {'CA': 1, 'A': [+1, 0, 0, 0, 5, 1]},
      cycles = 2
    )
    self.check1(
      regs = {'A': [+1, 0, 0, 0, 0, 0]},
      memory = {0: [+1, 0, 0, 0, 5, 2]},
      diff = {'CA': 1, 'A': [-1, 0, 0, 0, 5, 2]},
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
      memory = {0: [+1, 0, 0, 0,28, 2]}, # 28 = (3:4)
      diff = {'CA': 1, 'A': [+1, 5, 4, 3, 1, 37]},
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
      regs = {'A': [+1, 5, 4, 3, 2, 1]},
      memory = {0: [+1, 0, 0, 0, 2, 2]}, # 2 = (0:2)
      diff = {'CA': 1},
      cycles = 2,
      message = "subtracting zero-part of word"
    )

    self.check1(
      regs = {'A': [-1, 63, 2, 0, 0, 3]},
      memory = {
        64  : [+1, 63, 2, 0, 0, 3],
        10 : [+1, 1, 0, 0, 5, 1]
      },
      startadr = 10,
      diff = {'CA': 11, 'A': [-1, 0, 0, 0, 0, 0]},
      cycles = 2,
      message = "saving sign of rA, if rA == 0"
    )
    self.check1(
      regs = {'A': [-1, 63, 2, 0, 0, 3]},
      memory = {
        0  : [-1, 63, 2, 0, 0, 3],
        10 : [+1, 0, 0, 0, 5, 2]
      },
      startadr = 10,
      diff = {'CA': 11, 'A': [-1, 0, 0, 0, 0, 0]},
      cycles = 2,
      message = "saving sign of rA, if rA == 0"
    )

    self.check1(
      regs = {'A': [+1, 63, 2, 0, 0, 3]},
      memory = {
        3  : [-1, 63, 2, 0, 0, 3],
        10 : [+1, 0, 3, 0, 5, 1]
      },
      startadr = 10,
      diff = {'CA': 11, 'A': [+1, 0, 0, 0, 0, 0]},
      cycles = 2,
      message = "saving sign of rA, if rA == 0"
    )
    self.check1(
      regs = {'A': [+1, 63, 2, 0, 0, 3]},
      memory = {
        0  : [+1, 63, 2, 0, 0, 3],
        10 : [+1, 0, 0, 0, 5, 2]
      },
      startadr = 10,
      diff = {'CA': 11, 'A': [+1, 0, 0, 0, 0, 0]},
      cycles = 2,
      message = "saving sign of rA, if rA == 0"
    )

    self.check1(
      regs = {'A': [+1, 63, 60, 60, 60, 60]},
      memory = {
        5  : [+1, 2, 3, 2, 1, 4],
        10 : [+1, 0, 5, 0, 5, 1]
      },
      startadr = 10,
      diff = {'CA': 11, 'OF' : 1, 'A': [+1, 1, 63, 62, 62, 0]},
      cycles = 2,
      message = "overflow test"
    )
    self.check1(
      regs = {'A': [+1, 63, 60, 60, 60, 60]},
      memory = {
        0  : [-1, 2, 3, 2, 1, 4],
        10 : [+1, 0, 0, 0, 5, 2]
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



    self.assertRaises(InvalidFieldSpec, self.exec1,
      memory = {0: [+1, 0, 0, 0,26, 1]} # 26 = (3:2)
    )
    self.assertRaises(InvalidFieldSpec, self.exec1,
      memory = {0: [+1, 0, 0, 0,26, 2]} # 26 = (3:2)
    )

    self.assertRaises(InvalidAddress, self.exec1,
      memory = {
        0  : [-1, 2, 3, 2, 1, 4],
        10 : [-1, 0, 1, 0, 5, 1]
      },
      startadr = 10
    )

    self.assertRaises(InvalidIndex, self.exec1,
      memory = {
        0  : [-1, 2, 3, 2, 1, 4],
        10 : [+1, 63, 1, 8, 5, 1]
      },
      startadr = 10
    )

suite = unittest.makeSuite(VMMathTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)
