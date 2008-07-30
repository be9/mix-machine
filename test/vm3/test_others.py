import unittest
from basetestcase import *

class VM3OthersTestCase(VM3BaseTestCase):
  def testNOP(self):
    self.check1(
      memory = { 0 : [+1, 63, 50, 44, 63, 0]},
      diff = {'CA' : 1},
      cycles = 1
    )

  def testHLT(self):
    self.check1(
      memory = { 0 : [+1, 63, 63, 63, 2, 5]},
      diff = {'CA' : 1, 'HLT' : 1},
      cycles = 10
    )

    self.check_hlt(
      memory = {
        0 : [+1, 0, 0, 0, 0, 0], # nop
        1 : [+1, 0, 0, 0, 2, 5],
      },
      diff = {'CA' : 2, 'HLT' : 1},
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
    pass

suite = unittest.makeSuite(VM3OthersTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)
