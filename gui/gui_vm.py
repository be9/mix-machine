from PyQt4.QtCore import *

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))

from virt_machine import *

class MemoryModel(QAbstractTableModel):
  def __init__(self, vm_data = None, parent = None):
    QAbstractTableModel.__init__(self, parent)
    if vm_data is not None:
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
      word = self.memory[index.row()]
      sign = "+" if word[0] == 1 else "-"
      return QVariant("%s %02i %02i %02i %02i %02i" % tuple([sign] + word[1:]))

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
