from PyQt4.QtGui import *
from PyQt4.QtCore import *

from devices_ui import Ui_Form

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))
from device import Device

class DevDockWidget(QDockWidget, Ui_Form):
  def __init__(self, parent = None):
    QDockWidget.__init__(self, parent)

    self.setWindowTitle(self.tr("Devices"))

    self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

    self.widget = QWidget(self)
    self.setupUi(self.widget)
    self.setWidget(self.widget)

class QTextEditDevice(Device):
  """Device that can read(write) from(to) QTextEdit widget"""
  def __init__(self, mode, block_size, lock_time, text_edit):
    #assert( ('r' in mode) ^ ('w' in mode) )
    assert('w' in mode and 'r' not in mode)
    Device.__init__(self, mode, block_size, lock_time)
    self.edit = text_edit
    self.edit.setPlainText("")

  #def read(self, limits):
    #"""Read from file minimum from one line or <block_size> chars"""
    #Device.read(self, limits)

    #line = self.file_object.readline().rstrip("\n\r")
    #if len(line) < self.block_size:
      #line += " " * (self.block_size - len(line))
    #else:
      #line = line[:self.block_size]
    #bytes = map(Device._ord, line)
    #return bytes

  def _addLine(self, line):
    self.edit.setPlainText(self.edit.toPlainText() + line + "\n")

  def write(self, bytes, limits):
    """Write <block_size> chars to file"""
    Device.write(self, bytes, limits)

    self._addLine( "".join(map(Device._chr, bytes)) )

  def control(self):
    """Jump to newline in file"""
    Device.control(self)

    if 'r' in self.mode:
      self.file_object.readline() # simply jump newline
    else: # 'w' in self.mode:
      self._addLine("<---------NEW-PAGE--------->")
