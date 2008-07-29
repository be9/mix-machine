import unittest
from basetestcase import *

class VM3LoadTestCase(VM3BaseTestCase):
  def testNormal(self):
    self.check1(
      memory = {
        10: [+1, 0, 50, 0, 5, 8],
        50: [-1, 0, 2, 5, 4, 1]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        'A' : [-1, 0, 2, 5, 4, 1]
      },
      cycles = 2
    )
    self.check1(
      memory = {
        10: [+1, 0, 50, 0, 5, 16],
        50: [-1, 0, 2, 5, 4, 1]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        'A' : [+1, 0, 2, 5, 4, 1]
      },
      cycles = 2
    )

    self.check1(
      memory = {
        10: [+1, 0, 50, 0, 13, 15], # 1:5
        50: [-1, 0, 2, 5, 4, 1]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        'X' : [+1, 0, 2, 5, 4, 1]
      },
      cycles = 2
    )
    self.check1(
      memory = {
        10: [+1, 0, 50, 0, 13, 23], # 1:5
        50: [-1, 0, 2, 5, 4, 1]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        'X' : [-1, 0, 2, 5, 4, 1]
      },
      cycles = 2
    )

    self.check1(
      memory = {
        10: [+1, 0, 50, 0, 0, 15], # 0:0
        50: [-1, 0, 2, 5, 4, 1]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        'X' : [-1, 0, 0, 0, 0, 0]
      },
      cycles = 2
    )
    self.check1(
      memory = {
        10: [+1, 0, 50, 0, 0, 23], # 0:0
        50: [-1, 0, 2, 5, 4, 1]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        'X' : [+1, 0, 0, 0, 0, 0]
      },
      cycles = 2
    )

    self.check1(
      memory = {
        10: [+1, 0, 50, 0, 20, 15], # 2:4
        50: [-1, 0, 2, 5, 4, 1]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        'X' : [+1, 0, 0, 2, 5, 4]
      },
      cycles = 2
    )
    self.check1(
      memory = {
        10: [+1, 0, 50, 0, 20, 23], # 2:4
        50: [-1, 0, 2, 5, 4, 1]
      },
      startadr = 10,
      diff = {
        'CA' : 11,
        'X' : [-1, 0, 0, 2, 5, 4]
      },
      cycles = 2
    )

    for i in xrange(1, 6+1):
      self.check1(
        memory = {
          10: [+1, 0, 50, 0, 20, 8+i], # 2:4
          50: [-1, 0, 2, 5, 4, 1]
        },
        startadr = 10,
        diff = {
          'CA' : 11,
          'I'+str(i) : [+1, 0, 0, 0, 5, 4]
        },
        cycles = 2
      )
      self.check1(
        memory = {
          10: [+1, 0, 50, 0, 20, 16+i], # 2:4
          50: [-1, 0, 2, 5, 4, 1]
        },
        startadr = 10,
        diff = {
          'CA' : 11,
          'I'+str(i) : [-1, 0, 0, 0, 5, 4]
        },
        cycles = 2
      )

  def testRaises(self):
    for c_code in xrange(8, 23+1):
      self.assertRaises(InvalidAddress, self.exec1,
        memory = {
          10 : [+1, 63, 63, 0, 5, c_code]
        },
        startadr = 10,
      )
      self.assertRaises(InvalidIndex, self.exec1,
        memory = {
          10 : [+1, 63, 63, 44, 5, c_code]
        },
        startadr = 10,
      )
      self.assertRaises(InvalidFieldSpec, self.exec1,
        memory = {
          10 : [+1, 3, 63, 0, 8, c_code] # 8 = 1:0
        },
        startadr = 10,
      )


suite = unittest.makeSuite(VM3LoadTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)
