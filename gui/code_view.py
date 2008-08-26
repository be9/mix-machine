from PyQt4.QtCore import *
from PyQt4.QtGui import *

import copy

class AbstractCodeView(QTableView):
  def init(self): # slot, not constructor!!!
    self.code_model = self.ModelClass(parent = self)
    self.setModel(self.code_model) # add model to set size of header
    self.horizontalHeader().setStretchLastSection(True) # for column with source line
    self.setSelectionMode(QAbstractItemView.NoSelection)

  def changeFont(self, new_font):
    self.setFont(new_font)
    font_metrics = QFontMetrics(self.font())
    addr = font_metrics.width("0000")
    word = font_metrics.width("+ 0000 00 00 00")

    h_header = self.horizontalHeader()
    h_header.setStretchLastSection(True) # for column with source line
    h_header.resizeSection(h_header.logicalIndex(0), addr + 20)
    h_header.resizeSection(h_header.logicalIndex(1), word + 20)

  def snapshotMem(self):
    """Takes a copy of mem to do diff it after run"""
    self.snap_mem = copy.deepcopy(self.code_model.words)

  def resetVM(self, vm_data, asm_data):
    self.code_model = self.ModelClass(vm_data, asm_data, self)
    self.setModel(self.code_model)
    self.caChanged()

  def updateVM(self, vm_data): # pure virtual
    pass

  def caChanged(self): # pure virtual
    pass

  def hook(self, item, old, new):
    self.code_model.hook(item, old, new)
    if item == "cur_addr":
      self.caChanged()
