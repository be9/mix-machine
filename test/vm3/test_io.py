import unittest
from basetestcase import *

class VM3IOTestCase(VM3BaseTestCase):
  def test(self):
    out_file = open("18.dev", "w")
    #in_file =  open("19.dev", "r")
    self.check_hlt(
      regs = {
        'W_LOCKED' : set([2000, 2001, 2002]),
        'RW_LOCKED' : set([3000, 3001, 3002])
      },
      memory = {
        0   : [+1, 2, 0, 0, 18, 37], # out 128(18)
        1   : [+1, 0, 1, 0, 18, 34], # jbus *
        2   : [+1, 0, 0, 0, 2, 5], # hlt
        128 : [+1, 0, 1, 2, 3, 4],
        129 : [+1, 5, 6, 7, 8, 9],
        130 : [+1,10,11,12,13,14],
        131 : [+1,15,16,17,18,19],
        132 : [+1,20,21,22,23,24],
        133 : [+1,25,26,27,28,29],
        134 : [+1,30,31,32,33,34],
        135 : [+1,35,36,37,38,39],
        136 : [+1,40,41,42,43,44],
        137 : [+1,45,46,47,48,49],
        138 : [+1,50,51,52,53,54],
        139 : [+1,55, 0, 0, 0, 0],
        140 : [+1, 0, 0, 0, 0, 0],
        141 : [+1, 0, 0, 0, 0, 0],
        142 : [+1, 0, 0, 0, 0, 0],
        143 : [+1, 0, 0, 0, 0, 0],
        144 : [+1, 0, 0, 0, 0, 0],
        145 : [+1, 0, 0, 0, 0, 0],
        146 : [+1, 0, 0, 0, 0, 0],
        147 : [+1, 0, 0, 0, 0, 0],
        148 : [+1, 0, 0, 0, 0, 0],
        149 : [+1, 0, 0, 0, 0, 0],
        150 : [+1, 0, 0, 0, 0, 0],
        151 : [+1, 0, 0, 0, 0, 0],
      },
      devs = {
        18 : (0, 'w', 24*5, 24*2, out_file),
        #19 : (0, 'r', 14*5, 14*2, in_file)
      },
      diff = {
        'CA' : 3,
        'J'  : [+1, 0, 0, 0, 0, 2],
        'HLT': 1
      },
      cycles = 59
    )
    out_file.close()
    out_file = open("18.dev", "r") 
    self.assertEqual(out_file.read(), " ABCDEFGHI~JKLMNOPQR[#STUVWXYZ0123456789.,()+-*/=$<>@;:'"+" "*(120-56))
    out_file.close()

suite = unittest.makeSuite(VM3IOTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)
