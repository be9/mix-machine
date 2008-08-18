from PyQt4.QtGui import *
from PyQt4.QtCore import *

from devices_ui import Ui_Form

class DevDockWidget(QDockWidget, Ui_Form):
  def __init__(self, parent = None):
    QDockWidget.__init__(self, parent)

    self.setWindowTitle(self.tr("Devices"))

    self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

    self.widget = QWidget(self)
    self.setupUi(self.widget)
    self.setWidget(self.widget)
