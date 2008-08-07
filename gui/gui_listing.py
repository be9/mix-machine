from PyQt4.QtCore import *

#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'assembler'))

class ListingModel(QAbstractTableModel):
  def __init__(self, parent = None):
    QAbstractTableModel.__init__(self, parent)

  def setListing(self, listing):
    self.listing = listing

  def rowCount(self, parent):
    return len(self.listing.lines)

  def columnCount(self, parent):
    return 2 # word, source-lines

  def data(self, index, role = Qt.DisplayRole):
    if not index.isValid():
      return QVariant()

    if role == Qt.TextAlignmentRole:
      if index.row() in (0, 1):
        # address or word
        return QVariant(Qt.AlignRight | Qt.AlignVCenter)
      else:
        return QVariant(Qt.AlignLeft | Qt.AlignVCenter)
    elif role == Qt.DisplayRole:
      listing_line = self.listing.lines[index.row()]
      column = index.column()

      if column == 0:
        return QVariant(listing_line.word2str())
      else:
        return QVariant(listing_line.line)
    else:
      return QVariant()

  def headerData(self, section, orientation, role = Qt.DisplayRole):
    if role == Qt.TextAlignmentRole:
      if orientation == Qt.Vertical:
        return QVariant(Qt.AlignRight | Qt.AlignVCenter)
    elif role == Qt.DisplayRole:
      if orientation == Qt.Horizontal:
        return QVariant(("Mix word", "Source line")[section])
      else:
        return QVariant(self.listing.lines[section].addr2str())
    else:
      return QVariant()