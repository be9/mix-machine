from PyQt4.QtGui import *
from PyQt4.QtCore import *

from word_edit import *

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))

from word import *

BASIC = 0
INDEX = 1
REGJ  = 2

class MixWordWidget(QLineEdit):
  def __init__(self, parent = None, type = BASIC):
    QLineEdit.__init__(self, parent)
    self.type = type
    self.setReadOnly(True)
    self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    self.setWord()
    self.connect(self, SIGNAL("textChanged(QString)"), self, SIGNAL("valueChanged()"))

  def setWord(self, word = None):
    self.word = Word(word)

    type = WORD
    if self.type == INDEX:
      self.word[1:3] = 0
    elif self.type == REGJ:
      self.word[0:3] = 0
      type = INT

    self.setText(     word2str(self.word, type, self.type)  )
    self.setToolTip(  word2toolTip(self.word, self.type)    )

  def mouseDoubleClickEvent(self, event): # overload doubleclick event
    word_edit = WordEdit(self.word, self.type, self)
    if word_edit.exec_():
      self.setWord(word_edit.word)
