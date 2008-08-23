from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MixTabs(QTabWidget):
  def __init__(self, parent = None):
    QTabWidget.__init__(self, parent)

  def showRun(self):
    self.setTabEnabled(1, True)
    self.setTabEnabled(2, True)
    self.setCurrentIndex(1)

  def hideRun(self):
    self.setTabEnabled(1, False)
    self.setTabEnabled(2, False)
    self.setCurrentIndex(0)
