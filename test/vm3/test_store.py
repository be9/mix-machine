import unittest
from basetestcase import *

class VM3StoreTestCase(VM3BaseTestCase):
  def testNormal(self):
    self.check1(
      memory = {
        10: [+1, 0, 50, 0, 2, 33], # stz 0:2
        50: [-1, 1, 2, 3, 4, 5]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        50 : [+1, 0, 0, 3, 4, 5]
      },
      cycles = 2
    )
    self.check1(
      memory = {
        10: [+1, 0, 50, 0, 10, 33], # stz 1:2
        50: [-1, 1, 2, 3, 4, 5]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        50 : [-1, 0, 0, 3, 4, 5]
      },
      cycles = 2
    )

    self.check1(
      regs = { 'A' : [-1, 10, 20, 30, 40, 50]},
      memory = {
        10: [+1, 0, 50, 0, 2, 24], # sta 0:2
        50: [+1, 1, 2, 3, 4, 5]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        50 : [-1, 40, 50, 3, 4, 5]
      },
      cycles = 2
    )

    self.check1(
      regs = { 'A' : [-1, 10, 20, 30, 40, 50]},
      memory = {
        10: [+1, 0, 50, 0, 29, 24], # sta 3:5
        50: [-1, 1, 2, 3, 4, 5]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        50 : [-1, 1, 2, 30, 40, 50]
      },
      cycles = 2
    )
    self.check1(
      regs = { 'X' : [+1, 10, 20, 30, 40, 50]},
      memory = {
        10: [+1, 0, 50, 0, 2, 31], # stx 0:2
        50: [-1, 1, 2, 3, 4, 5]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        50 : [+1, 40, 50, 3, 4, 5]
      },
      cycles = 2
    )

    for i in xrange(1, 6+1):
      self.check1(
        regs = { 'I'+str(i) : [+1, 0, 0, 0, 40, 50]},
        memory = {
          10: [+1, 0, 50, 0, 4, 24+i], # sti 0:4
          50: [-1, 1, 2, 3, 4, 5]
        },
        startadr = 10,
        diff = {
          'CA' : 11,
          50 : [+1, 0, 0, 40, 50, 5]
        },
        cycles = 2
      )

  def testRaises(self):
    pass


suite = unittest.makeSuite(VM3StoreTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)
