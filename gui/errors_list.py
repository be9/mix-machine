from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ErrorsList(QListWidget):
  def __init__(self, parent = None):
    QListWidget.__init__(self, parent)
    self.connect(self, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.clickOnError)

  def setBuddyText(self, text_edit):
    self.buddy_text = text_edit

  def setErrors(self, type, errors_str):
    self.clear()
    self.addItems(errors_str)
    self.show()

  def clickOnError(self, item):
    line = unicode(item.text())
    line_num = int( line[0:line.find(':')] ) # cut all before ':'

    # find absolute position
    text = unicode(self.buddy_text.toPlainText())
    pos = 0
    for _ in xrange(line_num - 1):
      pos = text.find('\n', pos) + 1

    cursor = self.buddy_text.textCursor()
    cursor.setPosition(pos)
    cursor.select(QTextCursor.LineUnderCursor)
    self.buddy_text.setTextCursor(cursor)
