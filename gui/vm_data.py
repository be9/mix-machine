from PyQt4.QtCore import *

from word_edit import word2str, word2toolTip

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm'))

from virt_machine import *
import vm_errors

vmtest_errors = vm_errors.__dict__.values() # all vm errors

class VMData:
  def __init__(self, asm_data):
    self.vm = VMachine(asm_data.mem_list, asm_data.start_addr)
    self.listing = asm_data.listing
    self.vm_errors = vm_errors

  def mem(self, addr):
    return self.vm[addr]

  def setMem(self, addr, word):
    self.vm[addr] = word

  def ca(self):
    return self.vm.cur_addr

  def cycles(self):
    return self.vm.cycles

  def halted(self):
    return self.vm.halted

  def step(self):
    self.vm.step()

  def is_readable(self, addr):
    return self.vm.is_readable(addr)

  def is_writeable(self, addr):
    return self.vm.is_writeable(addr)

  def setCPUHook(self, hook):
    self.vm.set_cpu_hook(hook)

  def setMemHook(self, hook):
    self.vm.set_mem_hook(hook)

  def setLockHook(self, hook):
    self.vm.set_lock_hook(hook)

  def addDevice(self, number, device):
    self.vm.set_device(number, device)
