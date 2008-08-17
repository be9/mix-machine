from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))
from word import Word

class ListingModel(QAbstractTableModel):
  def __init__(self, vm_data = None, parent = None):
    QAbstractTableModel.__init__(self, parent)
    if vm_data is not None:
      self.lines = vm_data.listing.lines[:]
      # new lines where word is Word (class), not list
      for line in self.lines:
        line.modified = False
        if line.addr != None:
          line.word = Word(line.word)

      self.is_readable = vm_data.is_readable
      self.create_addr2num_data() # creates data for addr2num(...)
      self.current_line = self.addr2num(vm_data.ca())
      self.inited = True
    else:
      self.inited = False

  def rowCount(self, parent):
    if self.inited:
      return len(self.lines)
    else:
      return 0

  def columnCount(self, parent):
    return 3 # addr, word, source-lines

  def data(self, index, role = Qt.DisplayRole):
    if not index.isValid():
      return QVariant()

    if role == Qt.TextAlignmentRole:
      if index.column() in (0,1):
        # address, mix word
        return QVariant(Qt.AlignHCenter | Qt.AlignVCenter)
      else:
        # source line
        return QVariant(Qt.AlignLeft | Qt.AlignVCenter)

    elif role == Qt.BackgroundRole:
      changed_row = self.lines[index.row()].modified
      ca_row = index.row() == self.current_line
      locked_row = not self.is_readable(self.lines[index.row()].addr)
      if changed_row and ca_row and locked_row:
        return QVariant(QColor(200, 150, 0))

      elif changed_row and ca_row:
        return QVariant(QColor(220, 220, 0))
      elif changed_row and locked_row:
        return QVariant(QColor(200, 25, 0))
      elif locked_row and ca_row:
        return QVariant(QColor(255, 175, 0))

      elif changed_row:
        return QVariant(QColor(160, 160, 164)) # gray - #a0a0a4
      elif ca_row:
        return QVariant(QColor(255, 255, 0))
      elif locked_row:
        return QVariant(QColor(255, 50, 0))
      else:
        return QVariant()

    elif role == Qt.DisplayRole:
      listing_line = self.lines[index.row()]
      column = index.column()

      if column == 0:
        if listing_line.addr is not None:
          return QVariant(listing_line.addr2str())
        else:
          return QVariant(u"")

      elif column == 1:
        if listing_line.addr is not None:
          if self.is_readable(listing_line.addr):
            return QVariant(listing_line.word.addr_str()) # print first two bytes as one address
          else:
            return QVariant(self.tr("LOCKED"))
        else:
          return QVariant(u"")

      else:
        return QVariant(listing_line.line)

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
        return QVariant(self.tr(("Addr", "Mix word", "Source line")[section]))
      else:
        return QVariant(str(section + 1))
    else:
      return QVariant()

  def lineChanged(self, num):
    """dataChange for all line"""
    self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"),
        self.index(num-1, 0),
        self.index(num-1, 2))

  def hook(self, item, old, new):
    if item == "cur_addr":
      old_num = self.addr2num(old)
      if old_num is not None:
        self.lineChanged(old_num)
      self.current_line = num = self.addr2num(new)
      if num is None:
        return
    elif isinstance(item, int):
      num = self.addr2num(item)
      if num is None:
        return
      self.lines[num].word = new
      self.lines[num].modified = True
    else:
      return # any cpu hook but cur_addr
    # dataChange for all line
    self.lineChanged(num)

  def create_addr2num_data(self):
    self.addr2num_data = dict([
        (self.lines[i].addr, i)
        for i in xrange(len(self.lines)) if self.lines[i].addr is not None
    ])

  def addr2num(self, addr):
    return self.addr2num_data.get(addr)
