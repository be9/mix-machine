from __future__ import with_statement

import unittest, sys, os, fnmatch

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parse_line import parse_lines
from errors import *
from assemble import Assembler

class CompleteProgramsTestCase(unittest.TestCase):
  def test(self):
    dir = os.path.join(os.path.dirname(__file__), 'mix_programs')
 
    #IGNORED = 'isains.mix Test.mix FloatOverflow.mix 1_3_2_Ex14.mix primes.mix 1_3_2_ProgM_ex3.mix'.split()
    IGNORED = []

    for fn in os.listdir(dir):
        if fnmatch.fnmatch(fn, '*.mix') and fn not in IGNORED:
          self.current_file = fn
          self.assemble_program(os.path.join(dir, fn))

  def assemble_program(self, fname):
    with open(fname, "r") as f:
      lines, errors = parse_lines(f.readlines())
      self.assertEqual(errors, [])

      asm = Assembler()
      asm.run(lines)

      self.assertEqual(asm.errors, [])

  def __str__(self):
    return "%s (%s), %s" % (self._testMethodName, self.__class__.__name__, self.current_file)

suite = unittest.makeSuite(CompleteProgramsTestCase, 'test')

if __name__ == "__main__":
	unittest.main()

