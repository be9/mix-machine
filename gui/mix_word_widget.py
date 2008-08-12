from PyQt4.QtGui import *
from PyQt4.QtCore import *

from cell_edit import CellEdit

class MixWordWidget(QLineEdit):
  def __init__(self, parent = None):
    QLineEdit.__init__(self, "+ 00 00 00 00 00", parent)
    self.setReadOnly(True)
    self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

  def mouseDoubleClickEvent(self, event): # overload doubleclick event
    self.emit(SIGNAL("doubleClicked()"))


if __name__ == "__main__":
  def test_double_click():
    print "Double-clicked!"
  import sys
  app = QApplication(sys.argv)

  mix_word = MixWordWidget(None)
  mix_word.show()
  app.connect(mix_word, SIGNAL("doubleClicked()"), test_double_click)

  sys.exit(app.exec_())