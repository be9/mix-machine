from PyQt4.QtCore import *
from PyQt4.QtGui import *

from word_edit import word2toolTip

class DisassemblerModel(QAbstractTableModel):
  def __init__(self, vm_data = None, parent = None):
    QAbstractTableModel.__init__(self, parent)
    if vm_data is not None:
      self.words = vm_data.vm
      self.mem_len = vm_data.vm.MEMORY_SIZE
      self.modified = [False for _ in xrange(self.mem_len)]
      self.is_readable = vm_data.is_readable
      self.is_locked = lambda x: not (vm_data.is_readable(x) and vm_data.is_writeable(x))
      self.ca = vm_data.ca()
      self.inited = True
    else:
      self.inited = False

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
          return QVariant(self.tr("NOP 0"))
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
        return QVariant()#str(section))
    else:
      return QVariant()

  def lineChanged(self, addr):
    """dataChange for all line"""
    self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"),
        self.index(addr, 0),
        self.index(addr, 3))

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
        self.lineChanged(adr)
    # else any cpu hook but cur_addr

