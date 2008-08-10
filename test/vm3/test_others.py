import unittest
from basetestcase import *

class VM3OthersTestCase(VM3BaseTestCase):
  def testCommonErrors(self):
    self.assertRaises(InvalidCA, self.exec1,
      startadr = 4000
    )
    self.assertRaises(InvalidCA, self.exec_hlt,
      memory = {
        3999 : [+1, 0, 0, 0, 0, 0] # NOP
      },
      startadr = 3999
    )

    for c, f in ((46, 6), (48, 4), (55, 4), (6, 6), (5, 3)):
      self.assertRaises(UnknownInstruction, self.exec1,
        memory = {
          0 : [+1, 0, 0, 0, f, c]
        }
      )

  def testNOP(self):
    self.check1(
      memory = { 0 : [+1, 63, 50, 44, 63, 0]},
      diff = {'CA' : 1},
      cycles = 1
    )

  def testHLT(self):
    self.check1(
      memory = { 0 : [+1, 63, 63, 63, 2, 5]},
      diff = {'HLT' : 1},
      cycles = 10
    )

    self.check_hlt(
      memory = {
        0 : [+1, 0, 0, 0, 0, 0], # nop
        1 : [+1, 0, 0, 0, 2, 5],
      },
      diff = {'CA' : 1, 'HLT' : 1},
      cycles = 11
    )

  def testNUMandCHAR(self):
    self.check1(
      regs = {'A' : [-1, 11, 32, 53, 34,  5], 'X' : [+1, 36, 57, 18, 39, 20]},
      memory = { 0 : [+1, 63, 63, 63, 0, 5]},
      diff = {'CA' : 1, 'A' : [-1, 9, 37, 32, 11, 18]},
      cycles = 10
    )
    self.check1(
      regs = {'A' : [-1, 9, 37, 32, 11, 18], 'X' : [+1, 43, 3, 43, 23, 61]},
      memory = { 0 : [+1, 63, 63, 63, 1, 5]},
      diff = {'CA' : 1, 'A' : [-1, 30, 31, 36, 30, 38], 'X' : [+1, 32, 36, 30, 36, 36]},
      cycles = 10
    )

  def testMOVE(self):
    self.check1(
      regs = {
        'I1' : [+1, 0, 0, 0, 1, 0]
      },
      memory = {
        0 : [+1, 0, 0, 0, 2, 7],
        1 : [-1, 1, 2, 3, 4, 5]
      },
      diff = {
        'CA' : 1,
        'I1': [+1, 0, 0, 0, 1, 2],
        64+0 : [+1, 0, 0, 0, 2, 7],
        64+1 : [-1, 1, 2, 3, 4, 5]
      },
      cycles = 5,
      message = "move 2 from 0 to 64"
    )

    self.check1(
      regs = {
        'I1' : [+1, 0, 0, 0, 1, 0]
      },
      memory = {
        0 : [+1, 0, 3, 0, 10, 7],
        3 : [-1, 1, 0, 9, 8, 7],
        4 : [+1, 2, 1, 0, 9, 8],
        5 : [-1, 3, 2, 1, 0, 9],
        6 : [+1, 4, 3, 2, 1, 0],
        7 : [-1, 5, 4, 3, 2, 1],
        8 : [+1, 6, 5, 4, 3, 2],
        9 : [-1, 7, 6, 5, 4, 3],
        10: [+1, 8, 7, 6, 5, 4],
        11: [-1, 9, 8, 7, 6, 5],
        12: [+1, 0, 9, 8, 7, 6],
      },
      diff = {
        'CA' : 1,
        'I1': [+1, 0, 0, 0, 1, 10],
        64+0 : [-1, 1, 0, 9, 8, 7],
        64+1 : [+1, 2, 1, 0, 9, 8],
        64+2 : [-1, 3, 2, 1, 0, 9],
        64+3 : [+1, 4, 3, 2, 1, 0],
        64+4 : [-1, 5, 4, 3, 2, 1],
        64+5 : [+1, 6, 5, 4, 3, 2],
        64+6 : [-1, 7, 6, 5, 4, 3],
        64+7 : [+1, 8, 7, 6, 5, 4],
        64+8 : [-1, 9, 8, 7, 6, 5],
        64+9 : [+1, 0, 9, 8, 7, 6],
      },
      cycles = 21,
      message = "move 10 from 3 to 64"
    )
    self.check1(
      regs = {
        'I1' : [+1, 0, 0, 0, 0, 1]
      },
      memory = {
        0 : [+1, 0, 0, 0, 2, 7],
        1 : [-1, 1, 2, 3, 4, 5]
      },
      diff = {
        'CA' : 1,
        'I1': [+1, 0, 0, 0, 0, 3],
        1+0 : [+1, 0, 0, 0, 2, 7],
        1+1 : [+1, 0, 0, 0, 2, 7]
      },
      cycles = 5,
      message = "move 2 from 0 to 1 (overlapping of regions)"
    )
    self.check1(
      regs = {
        'I1' : [+1, 0, 0, 0, 0, 0]
      },
      memory = {
        0 : [+1, 0, 1, 0, 2, 7],
        1 : [-1, 1, 2, 3, 4, 5],
        2 : [+1, 5, 6, 7, 8, 9]
      },
      diff = {
        'CA' : 1,
        'I1': [+1, 0, 0, 0, 0, 2],
        0+0 : [-1, 1, 2, 3, 4, 5],
        0+1 : [+1, 5, 6, 7, 8, 9]
      },
      cycles = 5,
      message = "move 2 from 1 to 0 (overlapping of regions)"
    )

    self.check1(
      memory = {
        0 : [+1, 0, 1, 0, 0, 7]
      },
      diff = {
        'CA' : 1
      },
      cycles = 1,
      message = "move 0"
    )
    self.check1(
      memory = {
        0 : [-1, 0, 1, 0, 0, 7]
      },
      diff = {
        'CA' : 1
      },
      cycles = 1,
      message = "move 0"
    )

    self.assertRaises(InvalidAddress, self.exec1,
      regs = { 'I1' : [+1, 0, 0, 0, 0, 1] },
      memory = { 0: [-1, 0, 1, 0, 5, 7] }
    )
    self.assertRaises(InvalidIndex, self.exec1,
      regs = { 'I1' : [+1, 0, 0, 0, 0, 1] },
      memory = { 0: [-1, 0, 1, 64, 5, 7] }
    )
    self.assertRaises(InvalidMove, self.exec1,
      regs = { 'I1' : [-1, 0, 0, 0, 0, 1] },
      memory = { 0: [+1, 0, 1, 0, 5, 7] }
    )
    self.assertRaises(InvalidMove, self.exec1,
      regs = { 'I1' : [+1, 0, 0, 0, 62, 30] },
      memory = { 0: [+1, 0, 1, 0, 10, 7] }
    )


suite = unittest.makeSuite(VM3OthersTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)
