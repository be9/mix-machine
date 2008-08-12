from PyQt4.QtGui import *
from PyQt4.QtCore import *

from word_edit import WordEdit

import gui_vm

class MemoryDockWidget(QDockWidget):
  def __init__(self, parent = None):
    QDockWidget.__init__(self, parent)
    self.setWindowTitle(self.tr("Memory"))

    self.mem_view = QTableView(self)
    self.mem_view.setModel(gui_vm.MemoryModel(parent = self))
    self.mem_view.horizontalHeader().setStretchLastSection(True)

    self.setWidget(self.mem_view)

    self.connect(self.mem_view, SIGNAL("doubleClicked(QModelIndex)"), self.slot_mem_view_edit)

  def initModel(self, vm_data):
    self.vm_data = vm_data
    self.model = gui_vm.MemoryModel(vm_data = self.vm_data, parent = self)
    self.mem_view.setModel(self.model)

  def slot_mem_view_edit(self, index):
    cell_edit = WordEdit(self.vm_data.mem(index.row()), index.row(), self)
    if cell_edit.exec_():
      self.vm_data.setMem(index.row(), cell_edit.word)

  def memChanged(self):
    indexTopLeft = self.model.index(0, 0)
    indexBottomRight = self.model.index(self.model.rowCount(None) - 1, 0)
    self.model.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), indexTopLeft, indexBottomRight)
