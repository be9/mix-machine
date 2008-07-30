import unittest
from basetestcase import *

class VM3AddrManipTestCase(VM3BaseTestCase):
  def testENTandENN(self):
    # testing normal work
    indexes = "A I1 I2 I3 I4 I5 I6 X".split()
    for i in xrange(len(indexes)):
      index = indexes[i]
      self.check1(
        memory = { 0 : [-1, 33, 44, 0, 2, 48 + i]}, # ent
        diff = {
          'CA' : 1,
          index : [-1, 0, 0, 0, 33, 44]
        },
        cycles = 1
      )
      self.check1(
        memory = { 0 : [-1, 33, 44, 0, 3, 48 + i]}, # enn
        diff = {
          'CA' : 1,
          index : [+1, 0, 0, 0, 33, 44]
        },
        cycles = 1
      )

    self.check1(
      memory = { 0 : [-1, 0, 0, 0, 2, 49]}, # ent
      diff = {
        'CA' : 1,
        'I1' : [-1, 0, 0, 0, 0, 0]
      },
      cycles = 1,
      message = "testing sign if M == 0"
    )
    self.check1(
      memory = { 0 : [+1, 0, 0, 0, 3, 51]}, # enn
      diff = {
        'CA' : 1,
        'I3' : [-1, 0, 0, 0, 0, 0]
      },
      cycles = 1,
      message = "testing sign if M == 0"
    )

    self.check1(
      regs = { 'I4' : [+1, 0, 0, 0, 0, 66]},
      memory = { 0 : [+1, 63, 63, 4, 2, 55]}, # ent
      diff = {
        'CA' : 1,
        'X' : [+1, 0, 0, 0, 1, 1],
        'OF' : 1
      },
      cycles = 1,
      message = "testing overflow"
    )
    self.check1(
      regs = { 'I4' : [-1, 0, 0, 0, 0, 2]},
      memory = { 0 : [-1, 63, 63, 4, 3, 55]}, # enn
      diff = {
        'CA' : 1,
        'X' : [+1, 0, 0, 0, 0, 1],
        'OF' : 1
      },
      cycles = 1,
      message = "testing negative overflow"
    )

  def testINCandDEC(self):
    # testing normal work
    indexes = "A I1 I2 I3 I4 I5 I6 X".split()
    for i in xrange(len(indexes)):
      index = indexes[i]
      self.check1(
        regs = { index : [-1, 0, 0, 0, 55, 44] },
        memory = { 0 : [-1, 2, 3, 0, 0, 48 + i]}, # inc
        diff = {
          'CA' : 1,
          index : [-1, 0, 0, 0, 57, 47]
        },
        cycles = 1
      )
      self.check1(
        regs = { index : [1, 0, 0, 0, 55, 44] },
        memory = { 0 : [-1, 2, 3, 0, 1, 48 + i]}, # dec
        diff = {
          'CA' : 1,
          index : [+1, 0, 0, 0, 57, 47]
        },
        cycles = 1
      )

    self.check1(
      regs = { 'I3' : [1, 0, 0, 0, 55, 44] },
      memory = { 0 : [-1, 55, 44, 0, 0, 51]}, # inc
      diff = {
        'CA' : 1,
        'I3' : [1, 0, 0, 0, 0, 0]
      },
      cycles = 1,
      message = "saving sign if result == 0"
    )
    self.check1(
      regs = { 'I3' : [-1, 0, 0, 0, 55, 44] },
      memory = { 0 : [-1, 55, 44, 0, 1, 51]}, # dec
      diff = {
        'CA' : 1,
        'I3' : [-1, 0, 0, 0, 0, 0]
      },
      cycles = 1,
      message = "saving sign if result == 0"
    )
    self.check1(
      regs = { 'I3' : [1, 0, 0, 0, 55, 44] },
      memory = { 0 : [1, 55, 44, 0, 1, 51]}, # dec
      diff = {
        'CA' : 1,
        'I3' : [1, 0, 0, 0, 0, 0]
      },
      cycles = 1,
      message = "saving sign if result == 0"
    )

    self.check1(
      regs = { 'I3' : [1, 0, 0, 0, 55, 44] },
      memory = { 0 : [1, 55, 44, 0, 0, 51]}, # inc
      diff = {
        'CA' : 1,
        'I3' : [1, 0, 0, 0, 47, 24],
        'OF' : 1
      },
      cycles = 1,
      message = "testing overflow"
    )
    self.check1(
      regs = { 'I3' : [-1, 0, 0, 0, 55, 44] },
      memory = { 0 : [1, 55, 44, 0, 1, 51]}, # dec
      diff = {
        'CA' : 1,
        'I3' : [-1, 0, 0, 0, 47, 24],
        'OF' : 1
      },
      cycles = 1,
      message = "testing overflow"
    )

  def testRaises(self):
    # to test not all rI, but only one - it's faster
    for c_code in (48, 50, 55): # A, I2, X
      for f_code in xrange(4):
        self.assertRaises(InvalidIndex, self.exec1,
          memory = {
            0 : [+1, 63, 63, 44, f_code, c_code]
          }
        )

suite = unittest.makeSuite(VM3AddrManipTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)