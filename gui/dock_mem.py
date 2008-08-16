from PyQt4.QtGui import *
from PyQt4.QtCore import *

from word_edit import WordEdit, word2str, word2toolTip

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
    self.mem_view.setModel(MemoryModel(parent = self))
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
    self.model = MemoryModel(vm_data = self.vm_data, parent = self)
    self.mem_view.setModel(self.model)
    assert(vm_data.vm.MEMORY_SIZE == 4000)
    self.goto_word.setValidator(QRegExpValidator(QRegExp("[0-3]?[0-9]{1,3}"), self)) # 9, 99, 999, 3999
    self.goto_word.setText(str(self.vm_data.ca())) # mem_view will be set to this row too

  def slot_mem_view_edit(self, index):
    if not self.vm_data.is_writeable(index.row()):
      return QMessageBox.information(self, self.tr("Mix machine"), self.tr("This memory cell is locked for writing."))
    word_edit = WordEdit(self.vm_data.mem(index.row()), parent = self)
    if word_edit.exec_():
      self.vm_data.setMem(index.row(), word_edit.word)

  def hook(self, addr, old, new):
    self.model.memChanged(addr)


class MemoryModel(QAbstractTableModel):
  def __init__(self, vm_data = None, parent = None):
    QAbstractTableModel.__init__(self, parent)
    if vm_data is not None:
      self.memory = vm_data.vm.memory
      self.is_readable = vm_data.is_readable
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
      if self.is_readable(index.row()):
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

  def memChanged(self, addr):
    index = self.index(addr, 0)
    self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
