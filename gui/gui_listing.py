from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))
from virt_machine import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'assembler'))
from listing import *

class ListingUpdatable_withWords(Listing):
  def __init__(self, vm_data):
    Listing.init_copy(self, vm_data.listing)
    for line in self.lines:
      if line.addr != None:
        line.word = Word(line.word)
    self.vm_data = vm_data

  def updateRow(self, num):
    """True - if row changed while running, else False"""
    addr = self.lines[num].addr
    if addr is None:
      return False
    if self.lines[num].word != self.vm_data.mem(addr):
      self.lines[num].word = Word(self.vm_data.mem(addr))
    return self.vm_data.is_addr_changed(addr)

class ListingModel(QAbstractTableModel):
  def __init__(self, vm_data = None, parent = None):
    QAbstractTableModel.__init__(self, parent)
    if vm_data is not None:
      self.vm_data = vm_data
      self.listing = ListingUpdatable_withWords(vm_data)
      self.inited = True
    else:
      self.inited = False

  def rowCount(self, parent):
    if self.inited:
      return len(self.listing.lines)
    else:
      return 0

  def columnCount(self, parent):
    return 3 # addr, word, source-lines

  def data(self, index, role = Qt.DisplayRole):
    if not index.isValid():
      return QVariant()

    changed_row = self.listing.updateRow(index.row())
    ca_row = self.listing.lines[index.row()].addr == self.vm_data.ca()

    if role == Qt.TextAlignmentRole:
      if index.column() in (0,1):
        # address, mix word
        return QVariant(Qt.AlignHCenter | Qt.AlignVCenter)
      else:
        # source line
        return QVariant(Qt.AlignLeft | Qt.AlignVCenter)

    elif role == Qt.BackgroundRole:
      if changed_row and ca_row:
        return QVariant(QColor(200, 200, 0))
      elif changed_row:
        return QVariant(QColor(200, 200, 200))
      elif ca_row:
        return QVariant(QColor(255, 255, 0))
      else:
        return QVariant()

    elif role == Qt.DisplayRole:
      listing_line = self.listing.lines[index.row()]
      column = index.column()

      if column == 0:
        if listing_line.addr is not None:
          return QVariant(listing_line.addr2str())
        else:
          return QVariant(u"")
      elif column == 1:
        if listing_line.addr is not None:
          self.listing.updateRow(index.row())
          return QVariant(listing_line.word.addr_str()) # print first two bytes as one address
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

  def memAndAddrChanged(self):
    # change all
    indexTopLeft = self.index(0, 0)
    indexBottomRight = self.index(self.rowCount(None) - 1, 2)
    self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), indexTopLeft, indexBottomRight)

  def find_strnum_by_addr(self, addr):
    lines = self.listing.lines
    for i in xrange(len(lines)):
      if lines[i].addr == addr:
        return i + 1 # numbers of lines started from 1
    else:
      return None