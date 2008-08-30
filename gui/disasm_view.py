from PyQt4.QtCore import *
from PyQt4.QtGui import *

from word_edit import word2toolTip

from code_view import AbstractCodeView

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from disasm import Disasm

class DisassemblerView(AbstractCodeView):
  def __init__(self, parent = None):
    AbstractCodeView.__init__(self, parent)
    self.ModelClass = DisassemblerModel

  def updateVM(self, vm_data):
    for i in xrange(self.code_model.mem_len):
      if not self.code_model.modified[i] and self.snap_mem[i] != self.code_model.words[i]:
        self.code_model.modified[i] = True
        self.code_model.lineChanged(i)
    del self.snap_mem
    self.code_model.ca = vm_data.ca()
    self.caChanged()

  def caChanged(self):
    self.setCurrentIndex(self.code_model.index(self.code_model.ca, 0))

class DisassemblerModel(QAbstractTableModel):
  def __init__(self, vm_data = None, asm_data = None, parent = None):
    QAbstractTableModel.__init__(self, parent)
    if vm_data is not None:
      self.words = vm_data.vm.memory
      self.mem_len = vm_data.vm.MEMORY_SIZE
      self.modified = [False for _ in xrange(self.mem_len)]
      self.is_readable = vm_data.is_readable
      self.is_locked = lambda x: not (vm_data.is_readable(x) and vm_data.is_writeable(x))
      self.ca = vm_data.ca()

      self.symtable = asm_data.symtable
      self.end_addr = asm_data.end_address

      self.disasm = Disasm()
      self.inited = True
    else:
      self.inited = False

  def addBreakpoint(self, index):
    i = index.row()
    if i in self.breaks:
      self.breaks.remove(i)
    else:
      self.breaks.add(i)
    self.lineChanged(i)

  def rowCount(self, parent):
    if self.inited:
      return self.mem_len
    else:
      return 0

  def columnCount(self, parent):
    return 3 # addr, word, disasm line

  def data(self, index, role = Qt.DisplayRole):
    if not index.isValid():
      return QVariant()

    i = index.row()

    if role == Qt.TextAlignmentRole:
      if index.column() in (0,1):
        # address, mix word
        return QVariant(Qt.AlignHCenter | Qt.AlignVCenter)
      else:
        # disasm line
        return QVariant(Qt.AlignLeft | Qt.AlignVCenter)

    elif role == Qt.BackgroundRole:
      changed_row = self.modified[i]
      ca_row =  i == self.ca
      locked_row = self.is_locked(i)
      if changed_row and ca_row and locked_row:
        return QVariant(QColor(200, 150, 0))

      elif changed_row and ca_row:
        return QVariant(QColor(220, 220, 0))
      elif changed_row and locked_row:
        return QVariant(QColor(200, 25, 0))
      elif locked_row and ca_row:
        return QVariant(QColor(255, 175, 0))

      elif changed_row:
        return QVariant(QColor(Qt.lightGray))
      elif ca_row:
        return QVariant(QColor(255, 255, 0))
      elif locked_row:
        return QVariant(QColor(255, 50, 0))
      else:
        return QVariant()

    elif role == Qt.DisplayRole:
      if index.column() == 0:
        return QVariant(str(i))

      elif index.column() == 1:
        if self.is_readable(i):
          return QVariant(self.words[i].addr_str()) # print first two bytes as one address
        else:
          return QVariant(self.tr("LOCKED"))

      else:
        if self.is_readable(i):
          return QVariant(self.disasm.disasm2str(self.words[i], i, self.symtable, self.end_addr, "\t"))
        else:
          return QVariant(self.tr("LOCKED"))

    elif role == Qt.ToolTipRole:
        if index.column() == 1:
          if self.is_readable(i):
            return QVariant(word2toolTip( self.words[i] ))
          else:
            return QVariant(self.tr("This memory cell is locked for reading"))
        else:
          return QVariant()

    else:
      return QVariant()

  def headerData(self, section, orientation, role = Qt.DisplayRole):
    if role == Qt.TextAlignmentRole:
      if orientation == Qt.Vertical:
        return QVariant(Qt.AlignRight | Qt.AlignVCenter)
      else:
        return QVariant(Qt.AlignHCenter | Qt.AlignVCenter)
    elif role == Qt.DisplayRole:
      if orientation == Qt.Horizontal:
        return QVariant(self.tr(("Addr", "Mix word", "Disassemled word")[section]))
      else:
        return QVariant(u"     ")#str(section))
    elif role == Qt.BackgroundRole and orientation == Qt.Vertical and section in self.breaks:
      # breakpoint
      return QVariant(QColor(Qt.red))
    else:
      return QVariant()

  def lineChanged(self, addr):
    """dataChange for all line"""
    self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"),
        self.index(addr, 0),
        self.index(addr, 3))
    self.emit(SIGNAL("headerDataChanged(Qt::Orientation, int, int)"),
        Qt.Vertical, addr, addr)

  def hook(self, item, old, new):
    if item == "cur_addr": # cpu hook
      self.ca = new
      self.lineChanged(old)
      self.lineChanged(new)
    elif isinstance(item, int): # mem hook
      self.modified[item] = True
      self.lineChanged(item)
    elif item in ("rw", "w"): # lock hook
      for addr in old.symmetric_difference(new):
        self.lineChanged(addr)
    # else any cpu hook but cur_addr

