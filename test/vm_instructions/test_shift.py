import unittest
from basetestcase import *

class VMShiftTestCase(VMBaseTestCase):
  def testSLAandSRA(self):
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5]},
      memory = { 0 : [+1, 0, 0, 0, 0, 6]}, # sla
      diff = {'CA' : 1},
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5]},
      memory = { 0 : [+1, 0, 0, 0, 1, 6]}, # sra
      diff = {'CA' : 1},
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5]},
      memory = { 0 : [+1, 0, 2, 0, 0, 6]}, # sla
      diff = {'CA' : 1, 'A' : [-1, 3, 4, 5, 0, 0] },
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5]},
      memory = { 0 : [+1, 0, 10, 0, 0, 6]}, # sla
      diff = {'CA' : 1, 'A' : [-1, 0, 0, 0, 0, 0] },
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5]},
      memory = { 0 : [+1, 0, 2, 0, 1, 6]}, # sra
      diff = {'CA' : 1, 'A' : [-1, 0, 0, 1, 2, 3] },
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5]},
      memory = { 0 : [+1, 0, 5, 0, 1, 6]}, # sra
      diff = {'CA' : 1, 'A' : [-1, 0, 0, 0, 0, 0] },
      cycles = 2,
    )

  def testSLAXandSRAX(self):
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5], 'X' : [+1, 6, 7, 8, 9, 0]},
      memory = { 0 : [+1, 0, 0, 0, 2, 6]}, # slax
      diff = {'CA' : 1},
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5], 'X' : [+1, 6, 7, 8, 9, 0]},
      memory = { 0 : [+1, 0, 0, 0, 3, 6]}, # slax
      diff = {'CA' : 1},
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5], 'X' : [+1, 6, 7, 8, 9, 0]},
      memory = { 0 : [+1, 0, 4, 0, 2, 6]}, # slax
      diff = {'CA' : 1, 'A' : [-1, 5, 6, 7, 8, 9], 'X' : [+1, 0, 0, 0, 0, 0]},
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5], 'X' : [+1, 6, 7, 8, 9, 0]},
      memory = { 0 : [+1, 0, 9, 0, 2, 6]}, # slax
      diff = {'CA' : 1, 'A' : [-1, 0, 0, 0, 0, 0], 'X' : [+1, 0, 0, 0, 0, 0]},
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5], 'X' : [+1, 6, 7, 8, 9, 0]},
      memory = { 0 : [+1, 0, 3, 0, 3, 6]}, # srax
      diff = {'CA' : 1, 'A' : [-1, 0, 0, 0, 1, 2], 'X' : [+1, 3, 4, 5, 6, 7]},
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5], 'X' : [+1, 6, 7, 8, 9, 0]},
      memory = { 0 : [+1, 0, 59, 0, 3, 6]}, # srax
      diff = {'CA' : 1, 'A' : [-1, 0, 0, 0, 0, 0], 'X' : [+1, 0, 0, 0, 0, 0]},
      cycles = 2,
    )

  def testSLCandSRC(self):
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5], 'X' : [+1, 6, 7, 8, 9, 0]},
      memory = { 0 : [-1, 0, 0, 0, 5, 6]}, # src
      diff = {'CA' : 1},
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5], 'X' : [+1, 6, 7, 8, 9, 0]},
      memory = { 0 : [+1, 0, 50, 0, 4, 6]}, # slc
      diff = {'CA' : 1},
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5], 'X' : [+1, 6, 7, 8, 9, 0]},
      memory = { 0 : [+1, 0, 33, 0, 4, 6]}, # slc
      diff = {'CA' : 1, 'A' : [-1, 4, 5, 6, 7, 8], 'X' : [+1, 9, 0, 1, 2, 3]},
      cycles = 2,
    )
    self.check1(
      regs = {'A' : [-1, 1, 2, 3, 4, 5], 'X' : [+1, 6, 7, 8, 9, 0]},
      memory = { 0 : [+1, 0, 28, 0, 5, 6]}, # src
      diff = {'CA' : 1, 'A' : [-1, 3, 4, 5, 6, 7], 'X' : [+1, 8, 9, 0, 1, 2]},
      cycles = 2,
    )

  def testRaises(self):
    for f_code in xrange(0, 5 + 1):
      self.assertRaises(NegativeShift, self.exec1,
        memory = {
          0 : [-1, 0, 3, 0, f_code, 6]
        }
      )
      self.assertRaises(InvalidIndex, self.exec1,
        memory = {
          0 : [+1, 0, 3, 9, f_code, 6]
        }
      )
      # what to do if M > 64**2 ? (Knuth haven't said anything )

suite = unittest.makeSuite(VMShiftTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)
