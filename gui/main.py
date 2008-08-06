#!/usr/bin/env python

from __future__ import with_statement

import sys
import os.path
import codecs

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from main_ui import Ui_MainWindow

import gui_asm

PROGRAM_NAME = "Mix Machine"

class MainWindow(QMainWindow, Ui_MainWindow):
  def __init__(self, parent=None):
    QMainWindow.__init__(self, parent)

    self.setAttribute(Qt.WA_DeleteOnClose)
    self.setupUi(self)

    self.file_filters = self.tr("MIX source files (*.mix);;All files (*.*)");
    self.setCurrentFile("")

    self.txt_source.setPlainText(u"")

    self.connect(self.action_Quit, SIGNAL("triggered()"), qApp, SLOT("closeAllWindows()"))
    self.connect(self.txt_source, SIGNAL("textChanged()"), lambda: self.setWindowModified(True))

    self.connect(self.action_Open, SIGNAL("triggered()"), self.slot_File_Open)
    self.connect(self.action_New, SIGNAL("triggered()"), self.slot_File_New)
    self.connect(self.action_Save, SIGNAL("triggered()"), self.slot_File_Save)
    self.connect(self.action_Save_as, SIGNAL("triggered()"), self.slot_File_SaveAs)

    self.connect(self.action_Assemble, SIGNAL("triggered()"), self.slot_Assemble)

    self.connect(self.errors_list, SIGNAL("itemDoubleClicked(QListWidgetItem *)"),
        self.slot_clickOnError)

    self.setRunTabsEnabled(False)
    self.errors_list.setVisible(False)

  def setRunTabsEnabled(self, enable):
    self.tabWidget.setTabEnabled(1, enable)
    self.tabWidget.setTabEnabled(2, enable)

  def setNewSource(self):
    self.setRunTabsEnabled(False)
    self.tabWidget.setCurrentIndex(0)

  def slot_File_New(self):
    if not self.checkUnsaved(): 
      return

    self.txt_source.setPlainText(u"")

    self.setWindowModified(False)

    self.setCurrentFile("")

    self.setNewSource()

    self.statusBar().showMessage(self.tr("Empty source file has been created."), 2000);

  def checkUnsaved(self):
    if not self.isWindowModified():
      return True

    button = QMessageBox.information(self, PROGRAM_NAME, \
        self.tr("Document was changed!"), \
        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

    if button == QMessageBox.Save:
      self.saveFile()
    elif button == QMessageBox.Cancel:
      return False

    return True

  def setCurrentFile(self, fname):
    self.cur_file = unicode(fname)

    self.setWindowModified(False)

    shown_name = self.tr("Untitled")

    if self.cur_file != "":
      path, shown_name = os.path.split(self.cur_file)

    self.setWindowTitle(self.trUtf8("%1[*] \xE2\x80\x94 %2").arg(shown_name, PROGRAM_NAME))

  def slot_File_Save(self):
    if self.cur_file == "":
      self.slot_File_SaveAs()
    else:
      self.saveToFile(self.cur_file)

  def slot_File_SaveAs(self):
    fn = QFileDialog.getSaveFileName(self, self.tr("Choose file to save to..."), \
        self.cur_file, self.file_filters)

    if fn != "":
      fn = unicode(QDir.toNativeSeparators(fn))    
      if self.saveToFile(fn):
        self.setCurrentFile(fn)

  def closeEvent(self, ce):
    if self.checkUnsaved():
      ce.accept()
    else:
      ce.ignore()

  def slot_File_Open(self):
    if not self.checkUnsaved():
      return

    fn = QFileDialog.getOpenFileName(self, self.tr("Open file..."), "", self.file_filters)

    if fn != "":
      self.loadFromFile(unicode(QDir.toNativeSeparators(fn)))

  def saveToFile(self, filename):
    try:
      base, ext = os.path.splitext(unicode(filename))

      if ext == '' or ext == '.':
        filename = base + '.mix'

      with codecs.open(filename, "w", "UTF-8") as f:
        f.write(unicode(self.txt_source.toPlainText()))

      self.setWindowModified(False)

      self.statusBar().showMessage(self.tr("File has been saved."), 2000)

    except IOError, (errno, errtext):
      QMessageBox.critical(None, self.tr("Error"), errtext)
      self.statusBar().showMessage(self.tr("Error saving file."), 2000)

    else:
      return True

    return False

  def loadFromFile(self, filename):
    try:
      with codecs.open(filename, "r", "UTF-8") as f:
        self.txt_source.setPlainText(f.read())
      
      self.setWindowModified(False)

    except IOError, (errno, errtext):
      QMessageBox.critical(None, self.tr("Error"), errtext)
      self.statusBar().showMessage(self.tr("Error loading file."), 2000)

    else:
      self.setNewSource()

      self.setCurrentFile(filename)

  def slot_Assemble(self):
    self.errors_list.setVisible(False)
    self.setRunTabsEnabled(False)
    ret_type, content = gui_asm.asm(unicode(self.txt_source.toPlainText()))
    if ret_type == gui_asm.NO_ERRORS:
      self.asm_data = content

      self.setRunTabsEnabled(True)
      self.listing_view.setPlainText(str(self.asm_data.listing))
      self.tabWidget.setCurrentIndex(1)
      self.statusBar().showMessage(self.tr("Source assembled succesfully"), 2000)
      return

    # we have errors!
    if ret_type == gui_asm.SYNTAX_ERRORS:
      err_mesg = self.tr("There are syntax errors")
    else:
      err_mesg = self.tr("There are assemble errors")

    # content - errors
    self.errors_list.clear()
    self.errors_list.addItems([ self.tr(str("%i: %s" % err)) for err in content ])
    self.errors_list.setVisible(True)

    self.statusBar().showMessage(err_mesg, 2000)

  def slot_clickOnError(self, item):
    line = unicode(item.text())
    line_num = int( line[0:line.find(':')] ) # cut all before ':'

    # find absolute position
    text = unicode(self.txt_source.toPlainText())
    pos = 0
    for _ in xrange(line_num - 1):
      pos = text.find('\n', pos) + 1

    cursor = self.txt_source.textCursor()
    cursor.setPosition(pos)
    cursor.select(QTextCursor.LineUnderCursor)
    self.txt_source.setTextCursor(cursor)

app = QApplication(sys.argv)

mw = MainWindow()
mw.show()
sys.exit(app.exec_())
