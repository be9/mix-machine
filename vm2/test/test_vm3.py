import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from vm3 import *
from word import *
from errors import *

class VM3TestCase(unittest.TestCase):
  def testLoadAndState(self):
    vm3 = VM3()
    mega = {
      0: [+1, 1, 2, 3, 4, 5],
      2000: [-1, 0, 0, 0, 0, 0],
      3999: [+1, 11 , 22, 33, 44, 55],
      'A': [+1, 1, 2, 3, 4, 5],
      'X': [-1, 0, 1, 2, 3, 4],
      'I1': [+1, 0, 0, 0, 2, 3],
      'I2': [-1, 0, 0, 0, 1, 2],
      'I3': [+1, 0, 0, 0, 0, 1],
      'I4': [-1, 0, 0, 0, 0, 0],
      'I5': [+1, 0, 0, 0, 3, 0],
      'I6': [-1, 0, 0, 0, 4, 3],
      'J': [+1, 0, 0, 0, 5, 4],
      'CA': 666,
      'CF': -1,
      'OF': 1,
      'HLT': 0
    }
    vm3.load(mega)
    self.assertTrue(vm3.vm.cmp_memory({
      0: Word([+1, 1, 2, 3, 4, 5]),
      2000: Word([-1, 0, 0, 0, 0, 0]),
      3999: Word([+1, 11 , 22, 33, 44, 55])
    }))
    self.assertEqual(vm3.vm.rA, Word(mega["A"]))
    self.assertEqual(vm3.vm.rX, Word(mega["X"]))
    self.assertEqual(vm3.vm.r1, Word(mega["I1"]))
    self.assertEqual(vm3.vm.r2, Word(mega["I2"]))
    self.assertEqual(vm3.vm.r3, Word(mega["I3"]))
    self.assertEqual(vm3.vm.r4, Word(mega["I4"]))
    self.assertEqual(vm3.vm.r5, Word(mega["I5"]))
    self.assertEqual(vm3.vm.r6, Word(mega["I6"]))
    self.assertEqual(vm3.vm.rJ, Word(mega["J"]))
    self.assertEqual(vm3.vm.cur_addr, mega["CA"])
    self.assertEqual(vm3.vm.cf, mega["CF"])
    self.assertEqual(int(vm3.vm.of), mega["OF"])
    self.assertEqual(int(vm3.vm.halted), mega["HLT"])

    new_mega = vm3.state()
    self.assertTrue(all(
      (i     in mega and new_mega[i] == mega[i]) or
      (i not in mega and new_mega[i] == [+1, 0, 0, 0, 0, 0])
      for i in xrange(vm3.vm.MEMORY_SIZE)
    ))
    for arg in "A X I1 I2 I3 I4 I5 I6 J CA CF OF HLT".split():
      self.assertEqual(mega[arg], new_mega[arg])


suite = unittest.makeSuite(VM3TestCase, 'test')

if __name__ == "__main__":
  unittest.main()
