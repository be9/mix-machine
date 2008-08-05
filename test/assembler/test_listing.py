import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'assembler'))
from listing import *

class ListingTestCase(unittest.TestCase):
  def testListingLine(self):
    ll = ListingLine()
    self.assertEqual(ll.addr, None)
    self.assertEqual(ll.word, None)
    self.assertEqual(ll.line, None)

    ll = ListingLine(word = 5)
    self.assertEqual(ll.addr, None)
    self.assertEqual(ll.word, 5)
    self.assertEqual(ll.line, None)

    ll = ListingLine(word = 5, line = 2, addr = 1)
    self.assertEqual(ll.addr, 1)
    self.assertEqual(ll.word, 5)
    self.assertEqual(ll.line, 2)

    ll = ListingLine(1, 5, 2)
    self.assertEqual(ll.addr, 1)
    self.assertEqual(ll.word, 5)
    self.assertEqual(ll.line, 2)

  def check(self, src, asm, mem, result):
    listing = Listing(src, asm, mem)
    #print "we have:"
    #print reduce(lambda x,y: str(x) + '\n' + str(y), listing.lines)
    #print "we wait:"
    #print reduce(lambda x,y: str(x) + '\n' + str(y), result)
    self.assertEqual(listing.lines, result)

  def test(self):
    self.check(
      src = """\
STart eNTA 3 this is start of my mega program
LABEL1 \tStA LABEL1 sample of self modified code
* i love this program

* empty lines


\toRIg 1000
 equ 18 device
9H hlt
 eND 0
 and this is my
 long
 long poem""".splitlines(),
      asm = [
        Line("START", "ENTA", "3", 1,         0),
        Line("LABEL1", "STA", "LABEL1", 2,    1),
        Line(None, "ORIG", "1000", 8),
        Line(None, "EQU", "18", 9),
        Line("9H", "HLT", None, 10,           1000),
        Line(None, "END", "0", 11)
      ],
      mem = {
        0 : [+1, 0, 3, 0, 2, 48],
        1 : [+1, 0, 1, 0, 5, 24],
        1000 : [+1, 0, 0, 0, 2, 5]
      },
      result = [
        ListingLine(   0, [+1, 0, 3, 0, 2, 48],     "STart eNTA 3 this is start of my mega program"),
        ListingLine(   1, [+1, 0, 1, 0, 5, 24],     "LABEL1 \tStA LABEL1 sample of self modified code"),
        ListingLine(None, None,                     "* i love this program"),
        ListingLine(None, None,                     ""),
        ListingLine(None, None,                     "* empty lines"),
        ListingLine(None, None,                     ""),
        ListingLine(None, None,                     ""),
        ListingLine(None, None,                     "\toRIg 1000"),
        ListingLine(None, None,                     " equ 18 device"),
        ListingLine(1000, [+1, 0, 0, 0, 2, 5],      "9H hlt"),
        ListingLine(None, None,                     " eND 0"),
        ListingLine(None, None,                     " and this is my"),
        ListingLine(None, None,                     " long"),
        ListingLine(None, None,                     " long poem")
      ]
    )
    
suite = unittest.makeSuite(ListingTestCase, 'test')

if __name__ == "__main__":
  unittest.main()
