from PyQt4.QtGui import *
from PyQt4.QtCore import *

from word_edit import WordEdit

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))

from word import *

class MixWordWidget(QLineEdit):
  def __init__(self, parent = None):
    QLineEdit.__init__(self, "+ 00 00 00 00 00", parent)
    self.setReadOnly(True)
    self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    self.word = Word()

  def setWord(self, word):
    self.word = Word(word)
    self.setText(str(self.word))

  def mouseDoubleClickEvent(self, event): # overload doubleclick event
    word_edit = WordEdit(self.word, self)
    if word_edit.exec_():
      self.setWord(word_edit.word)
      self.emit(SIGNAL("valueChanged()"))
