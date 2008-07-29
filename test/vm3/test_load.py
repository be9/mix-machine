import unittest
from basetestcase import *

class VM3LoadTestCase(VM3BaseTestCase):
  def test(self):
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

    

suite = unittest.makeSuite(VM3LoadTestCase, 'test')

if __name__ == "__main__":
  unittest.main()
