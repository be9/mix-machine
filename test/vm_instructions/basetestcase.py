import unittest
import copy

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'vm'))
from vmtest_errors import *

_initial_context = {
  'A': [+1, 11, 22, 33, 44, 55],
  'X': [-1, 22, 33, 44, 55, 11],
  'I1': [+1, 0, 0, 0, 10, 20],
  'I2': [-1, 0, 0, 0, 22, 33],
  'I3': [+1, 0, 0, 0, 63, 25],
  'I4': [-1, 0, 0, 0, 14, 7],
  'I5': [+1, 0, 0, 0, 23, 8],
  'I6': [-1, 0, 0, 0, 46, 51],
  'J':  [+1, 0, 0, 0, 37, 14],
  'CA': 0,
  'CF': 0,
  'OF': 0,
  'HLT': 0,
  'W_LOCKED' : set(),
  'RW_LOCKED' : set(),
}

class VMBaseTestCase(unittest.TestCase):
  @staticmethod
  def set_vm_class(klass):
    VMBaseTestCase.vm_class = klass

  def check1(self, regs = {}, memory = {}, devs = {}, startadr = 0, diff = {}, cycles = 0, message = None):
    self.assertEqual(self.exec1(regs, memory, devs, startadr), diff, message)
    self.assertEqual(self.cycles, cycles, message)

  def check_hlt(self, regs = {}, memory = {}, devs = {}, startadr = 0, diff = {}, cycles = 0, message = None):
    self.assertEqual(self.exec_hlt(regs, memory, devs, startadr), diff, message)
    self.assertEqual(self.cycles, cycles, message)

  def exec1(self, regs = {}, memory = {}, devs = {}, startadr = 0):
    return self.execute(regs, memory, devs, startadr, exec_at = True)

  def exec_hlt(self, regs = {}, memory = {}, devs = {}, startadr = 0):
    return self.execute(regs, memory, devs, startadr, exec_at = False)

  def setUp(self):
    self.vm = VMBaseTestCase.vm_class()

  def hook(self, item, old, new):
    self.diff[item] = new

  def init_vm(self, regs, memory, devs):
    ctx = copy.copy(_initial_context)
    
    # fill memory
    ctx.update(memory)

    # fill regs
    ctx.update(regs)


    self.vm.load(ctx, devs, self.hook)

  def execute(self, regs = {}, memory = {}, devs = {}, startadr = 0, exec_at = True):
    self.init_vm(regs, memory, devs)

    self.diff = {}
    if exec_at:
      self.cycles = self.vm.execute(at=startadr)
    else:
      self.cycles = self.vm.execute(start=startadr)

    return self.diff

# fill memory
def _memory_value(adr):
  num = hash(str(adr)) % (64**5)

  # stolen from VM2 Word
  mask = 63
  u_num = abs(num)

  sign = +1 if adr % 2 == 0 else -1

  return [sign] + [ (u_num >> shift) & mask for shift in xrange(24, -1, -6) ] # 24 = 6 * (5-1)

for adr in xrange(4000):
  _initial_context[adr] = _memory_value(adr)
