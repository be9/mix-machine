from PyQt4.QtGui import *
from PyQt4.QtCore import *

from word_edit import WordEdit

import gui_vm

class MemoryDockWidget(QDockWidget):
  def __init__(self, parent = None):
    QDockWidget.__init__(self, parent)
    self.setWindowTitle(self.tr("Memory"))

    self.widget = QWidget(self)

    self.goto_label = QLabel(self.tr("Goto:"), self.widget)
    self.goto_word = QLineEdit(self.widget)
    self.goto_word.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    self.goto_layout = QHBoxLayout()
    self.goto_layout.addWidget(self.goto_label)
    self.goto_layout.addWidget(self.goto_word)

    self.mem_view = QTableView(self.widget)
    self.mem_view.setModel(gui_vm.MemoryModel(parent = self))
    self.mem_view.horizontalHeader().setStretchLastSection(True)

    self.layout = QVBoxLayout()
    self.layout.addLayout(self.goto_layout)
    self.layout.addWidget(self.mem_view)

    self.widget.setLayout(self.layout)
    self.setWidget(self.widget)
    
    self.connect(self.mem_view, SIGNAL("pressed(QModelIndex)"),\
        lambda index: self.goto_word.setText(str(index.row())))
    self.connect(self.goto_word, SIGNAL("textChanged(QString)"),\
        lambda text:  self.mem_view.selectRow(int("0"+text))) # "0"+text - to avoid empty lines

    self.connect(self.mem_view, SIGNAL("doubleClicked(QModelIndex)"), self.slot_mem_view_edit)

  def initModel(self, vm_data):
    self.vm_data = vm_data
    self.model = gui_vm.MemoryModel(vm_data = self.vm_data, parent = self)
    self.mem_view.setModel(self.model)
    assert(vm_data.vm.MEMORY_SIZE == 4000)
    self.goto_word.setValidator(QRegExpValidator(QRegExp("[0-3]?[0-9]{1,3}"), self)) # 9, 99, 999, 3999
    self.goto_word.setText(str(self.vm_data.ca())) # mem_view will be set to this row too

  def slot_mem_view_edit(self, index):
    if not self.vm_data.is_writeable(index.row()):
      return QMessageBox.information(self, self.tr("Mix machine"), self.tr("This memory cell is locked for writing."))
    cell_edit = WordEdit(self.vm_data.mem(index.row()), parent = self)
    if cell_edit.exec_():
      self.vm_data.setMem(index.row(), cell_edit.word)

  def memChanged(self):
    indexTopLeft = self.model.index(0, 0)
    indexBottomRight = self.model.index(self.model.rowCount(None) - 1, 0)
    self.model.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), indexTopLeft, indexBottomRight)
