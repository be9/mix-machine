import unittest
from basetestcase import *

class VMCmpTestCase(VMBaseTestCase):
  def testNormal(self):
    # testing normal work
    indexes = {
      'A' : 56,
      'I2' : 58,
      'I6' : 62,
      'X' : 63
    }
    for index, c_code in indexes.items():
      self.check1(
        regs = { index : [-1, 1, 2, 3, 4, 5] },
        memory = {
          0 : [+1, 0, 10, 0, 5, c_code],
          10 : [+1, 3, 3, 3, 3, 3]
        },
        diff = { 'CA' : 1, 'CF' : -1},
        cycles = 2
      )
      self.check1(
        regs = { index : [-1, 1, 2, 3, 4, 5] },
        memory = {
          0 : [+1, 0, 10, 0, 5, c_code],
          10 : [-1, 3, 3, 3, 3, 3]
        },
        diff = { 'CA' : 1, 'CF' : 1},
        cycles = 2
      )
      self.check1(
        regs = { index : [-1, 1, 2, 3, 4, 5] },
        memory = {
          0 : [+1, 0, 10, 0, 27, c_code], # 3:3
          10 : [-1, 3, 3, 3, 3, 3]
        },
        diff = { 'CA' : 1},
        cycles = 2
      )

    self.check1(
      regs = { 'I3' : [-1, 1, 2, 3, 4, 5] },
      memory = {
        0 : [+1, 0, 10, 0, 13, 59], # 1:5
        10 : [-1, 3, 3, 3, 3, 3]
      },
      diff = { 'CA' : 1, 'CF' : -1},
      cycles = 2
    )
    self.check1(
      regs = { 'I4' : [-1, 0, 0, 3, 4, 5] },
      memory = {
        0 : [+1, 0, 10, 0, 2, 60], # 0:2
        10 : [+1, 0, 0, 3, 3, 3]
      },
      diff = { 'CA' : 1},
      cycles = 2
    )

  def testRaises(self):
    for c_code in (56, 58, 63):
      self.assertRaises(InvalidAddress, self.exec1,
        memory = {
          0 : [+1, 63, 63, 0, 5, c_code]
        }
      )
      self.assertRaises(InvalidIndex, self.exec1,
        memory = {
          0 : [+1, 63, 63, 44, 5, c_code]
        }
      )
      self.assertRaises(InvalidFieldSpec, self.exec1,
        memory = {
          0 : [+1, 3, 63, 0, 8, c_code] # 8 = 1:0
        }
      )

suite = unittest.makeSuite(VMCmpTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)
