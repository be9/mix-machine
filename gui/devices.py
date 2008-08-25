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

class QTextEditOutputDevice(Device):
  """Device that can write to QTextEdit widget"""
  def __init__(self, mode, block_size, lock_time, text_edit):
    assert('w' == mode)
    Device.__init__(self, mode, block_size, lock_time)
    self.edit = text_edit

  def _addLine(self, line):
    self.edit.setPlainText(self.edit.toPlainText() + line + "\n")

  def write(self, bytes, limits):
    """Write <block_size> chars"""
    Device.write(self, bytes, limits)
    self._addLine( "".join(map(Device._chr, bytes)) )

  def control(self):
    """Jump to newline"""
    Device.control(self)
    self._addLine("<---------NEW-PAGE--------->")

  def reset(self):
    self.edit.setPlainText("")

class QTextEditInputDevice(Device):
  """Device that can read from QTextEdit widget"""
  def __init__(self, mode, block_size, lock_time, text_edit):
    assert('r' == mode)
    Device.__init__(self, mode, block_size, lock_time)
    self.edit = text_edit

    self.read_lines = [] # lines that were read after last reset()

  def _readLine(self):
    lines = str(self.edit.toPlainText()).splitlines()
    if len(lines) == 0:
      return "" # empty TextEdit

    self.read_lines.append(lines[0])
    self.edit.setPlainText("\n".join(lines[1:])) # remove read line from TextEdit
    return lines[0]

  def read(self, limits):
    """Read minimum from one line and <block_size> chars"""
    Device.read(self, limits)
    line = self._readLine()
    if len(line) < self.block_size:
      line += " " * (self.block_size - len(line))
    else:
      line = line[:self.block_size]
    bytes = map(Device._ord, line)
    return bytes

  def control(self):
    """Jump to newline"""
    Device.control(self)
    self._readLine()

  def reset(self):
    # add all read lines to front of TextEdit
    text = "\n".join(self.read_lines)
    self.read_lines = []
    if len(self.edit.toPlainText()) != 0:
      if len(text) != 0:
        text += "\n"
      text += self.edit.toPlainText()
    self.edit.setPlainText(text)
