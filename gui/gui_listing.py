from PyQt4.QtCore import *

class ListingModel(QAbstractTableModel):
  def __init__(self, parent = None):
    QAbstractTableModel.__init__(self, parent)

  def setListing(self, listing):
    self.listing = listing

  def rowCount(self, parent):
    if self.listing is not None:
      return len(self.listing.lines)
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
        return QVariant(Qt.AlignCenter | Qt.AlignVCenter)
      else:
        # source line
        return QVariant(Qt.AlignLeft | Qt.AlignVCenter)
    elif role == Qt.DisplayRole:
      listing_line = self.listing.lines[index.row()]
      column = index.column()

      if column == 0:
        return QVariant(listing_line.addr2str())
      elif column == 1:
        return QVariant(listing_line.word2str_addr_bytes())
      else:
        return QVariant(listing_line.line)
    else:
      return QVariant()

  def headerData(self, section, orientation, role = Qt.DisplayRole):
    if role == Qt.TextAlignmentRole:
      if orientation == Qt.Vertical:
        return QVariant(Qt.AlignRight | Qt.AlignVCenter)
      else:
        return QVariant(Qt.AlignCenter | Qt.AlignVCenter)
    elif role == Qt.DisplayRole:
      if orientation == Qt.Horizontal:
        return QVariant(("Addr", "Mix word", "Source line")[section])
      else:
        return QVariant(str(section + 1))
    else:
      return QVariant()
