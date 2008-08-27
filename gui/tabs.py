from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MixTabs(QTabWidget):
  def __init__(self, parent = None):
    QTabWidget.__init__(self, parent)
    self.lastRunIndex = 1 # index of last used tab (1 - listing, 2 - disassembler)

  def showRun(self):
    self.setTabEnabled(1, True)
    self.setTabEnabled(2, True)
    self.setCurrentIndex(self.lastRunIndex)

  def hideRun(self):
    self.setTabEnabled(1, False)
    self.setTabEnabled(2, False)
    self.setCurrentIndex(0)

  def rememberRunTab(self):
    self.lastRunIndex = self.currentIndex()
