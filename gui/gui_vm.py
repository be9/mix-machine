from PyQt4.QtCore import *

from word_edit import word2str, word2toolTip

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))

from virt_machine import *
from word import *
from vm2_errors import *

class MemoryModel(QAbstractTableModel):
  def __init__(self, vm_data = None, parent = None):
    QAbstractTableModel.__init__(self, parent)
    if vm_data is not None:
      self.vm_data = vm_data
      self.memory = vm_data.vm.memory
      self.mem_len = vm_data.vm.MEMORY_SIZE
      self.inited = True
    else:
      self.inited = False

  def rowCount(self, parent):
    if self.inited:
      return self.mem_len
    else:
      return 0

  def columnCount(self, parent):
    return 1 # word

  def data(self, index, role = Qt.DisplayRole):
    if not index.isValid():
      return QVariant()

    if role == Qt.TextAlignmentRole:
      return QVariant(Qt.AlignHCenter | Qt.AlignVCenter)

    elif role == Qt.DisplayRole:
      if self.vm_data.is_readable(index.row()):
        return QVariant(  word2str(     self.memory[index.row()]  ))
      else:
        return QVariant(self.tr("LOCKED"))
    elif role == Qt.ToolTipRole:
      return QVariant(  word2toolTip( self.memory[index.row()]  ))

    else:
      return QVariant()

  def headerData(self, section, orientation, role = Qt.DisplayRole):
    if role == Qt.TextAlignmentRole:
      return QVariant(Qt.AlignHCenter | Qt.AlignVCenter)

    elif role == Qt.DisplayRole:
      if orientation == Qt.Horizontal:
        return QVariant(self.tr("Mix word"))
      else:
        return QVariant(str(section))

    else:
      return QVariant()

class VMData:
  def __init__(self, asm_data):
    self.vm = VMachine(asm_data.mem_list, asm_data.start_addr)
    self.listing = asm_data.listing

  def mem(self, addr):
    return self.vm.memory[addr]

  def setMem(self, addr, word):
    self.vm.memory[addr] = word

  def ca(self):
    return self.vm.cur_addr

  def halted(self):
    return self.vm.halted

  def step(self):
    self.vm.step()

  def run(self):
    while not self.vm.halted:
      self.vm.step()

  def is_readable(self, addr):
    return self.vm.is_readable(addr)

  def is_writeable(self, addr):
    return self.vm.is_writeable(addr)

  def setCPUHook(self, hook):
    self.vm.set_cpu_hook(hook)

  def setMemHook(self, hook):
    self.vm.set_mem_hook(hook)
