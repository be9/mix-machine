import unittest
from basetestcase import *

class VMJumpTestCase(VMBaseTestCase):
  def testBasic(self):
    self.check1(
      memory = { 0 : [+1, 2, 0, 0, 0, 39]},
      diff = {'CA' : 128, 'J' : [+1, 0, 0, 0, 0, 1] },
      cycles = 1,
      message = "JMP normal test"
    )
    self.check1(
      memory = { 0 : [+1, 2, 0, 0, 1, 39]},
      diff = {'CA' : 128},
      cycles = 1,
      message = "JSJ normal test"
    )

    self.check1(
      regs = { 'OF' : 1 },
      memory = { 0 : [+1, 2, 0, 0, 2, 39]},
      diff = {'CA' : 128, 'J' : [+1, 0, 0, 0, 0, 1], 'OF' : 0},
      cycles = 1,
      message = "JOV - jump"
    )
    self.check1(
      regs = { 'OF' : 0 },
      memory = { 0 : [+1, 2, 0, 0, 2, 39]},
      diff = {'CA' : 1},
      cycles = 1,
      message = "JOV - no jump"
    )
    self.check1(
      regs = { 'OF' : 0 },
      memory = { 0 : [+1, 2, 0, 0, 3, 39]},
      diff = {'CA' : 128, 'J' : [+1, 0, 0, 0, 0, 1]},
      cycles = 1,
      message = "JNOV - jump"
    )
    self.check1(
      regs = { 'OF' : 1 },
      memory = { 0 : [+1, 2, 0, 0, 3, 39]},
      diff = {'CA' : 1},
      cycles = 1,
      message = "JNOV - no jump"
    )

    for f_code in (0, 1):
      self.assertRaises(InvalidIndex, self.exec1,
        memory = {
          0 : [+1, 63, 63, 44, f_code, 39]
        }
      )
      self.assertRaises(InvalidAddress, self.exec1,
        memory = {
          0 : [+1, 63, 63, 0, f_code, 39]
        }
      )

  def testCFJumps(self):
    # for CF (KEY) jump will be done for instructions with f_codes in VALUES
    jumps = {
      -1 : (4, 8, 9),
      0  : (5, 7, 9),
      +1 : (6, 7, 8)
    }

    for cf in (-1, 0, 1):
      for f_code in xrange(4, 9 + 1):

        is_jump = f_code in jumps[cf]
        self.check1(
          regs = { 'CF' : cf },
          memory = { 0 : [+1, 2, 0, 0, f_code, 39]},
          diff = {'CA' : 128, 'J' : [+1, 0, 0, 0, 0, 1]} if is_jump else {'CA' : 1},
          cycles = 1,
          message = "f = %i (%sjump)" % (f_code, "" if is_jump else "no ")
        )
        if is_jump:
          self.assertRaises(InvalidIndex, self.exec1,
            regs = { 'CF' : cf },
            memory = {
              0 : [+1, 63, 63, 44, f_code, 39]
            }
          )
          self.assertRaises(InvalidAddress, self.exec1,
            regs = { 'CF' : cf },
            memory = {
              0 : [+1, 63, 63, 0, f_code, 39]
            }
          )

  def testRegJumps(self):
    # for reg (KEY) jump will be done for instructions with f_codes in VALUES
    jumps = {
      (-1, 0, 0, 0, 0, 1) : (0, 4, 5),
      (-1, 0, 0, 0, 0, 0) : (1, 3, 5),
      (+1, 0, 0, 0, 0, 0) : (1, 3, 5),
      (+1, 0, 0, 0, 0, 1) : (2, 3, 4)
    }
    c_codes = {
      'A' : 40,
      'I3' : 43,
      'X' : 47
    }
    for reg_value in jumps.keys():
      for reg in c_codes.keys():
        for f_code in xrange(0, 5 + 1):

          is_jump = f_code in jumps[reg_value]
          self.check1(
            regs = { reg : list(reg_value)},
            memory = { 0 : [+1, 2, 0, 0, f_code, c_codes[reg]]},
            diff = {'CA' : 128, 'J' : [+1, 0, 0, 0, 0, 1]} if is_jump else {'CA' : 1},
            cycles = 1,
            message = "c = %i (r%s = %s), f = %i (%sjump)" % (c_codes[reg], reg, reg_value, f_code, "" if is_jump else "no ")
          )
          if is_jump:
            self.assertRaises(InvalidIndex, self.exec1,
              regs = { reg : list(reg_value)},
              memory = {
                0 : [+1, 63, 63, 44, f_code, c_codes[reg]]
              }
            )
            self.assertRaises(InvalidAddress, self.exec1,
              regs = { reg : list(reg_value)},
              memory = {
                0 : [+1, 63, 63, 0, f_code, c_codes[reg]]
              }
            )

  def testOthers(self):
    self.check1(
      regs = { 'OF' : 1 },
      memory = { 0 : [-1, 63, 63, 63, 3, 39]},
      diff = {'CA' : 1},
      cycles = 1,
      message = "testing bad address (no jump)"
    )
    self.check1(
      regs = { 'CF' : -1},
      memory = { 0 : [-1, 63, 63, 63, 6, 39]},
      diff = {'CA' : 1},
      cycles = 1,
      message = "testing bad address (no jump)"
    )
    self.check1(
      regs = { 'I5' : [-1, 0, 0, 0, 0, 10]},
      memory = { 0 : [-1, 63, 63, 63, 3, 45]},
      diff = {'CA' : 1},
      cycles = 1,
      message = "testing bad address (no jump)"
    )

suite = unittest.makeSuite(VMJumpTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)
