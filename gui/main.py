#!/usr/bin/env python

from __future__ import with_statement

import sys
import os.path
import codecs

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from main_ui import Ui_MainWindow

from dock_mem import MemoryDockWidget
from dock_cpu import CPUDockWidget
from devices import DevDockWidget, QTextEditInputDevice, QTextEditOutputDevice

from asm_data import *
from vm_data import VMData

PROGRAM_NAME = "Mix Machine"

class MainWindow(QMainWindow, Ui_MainWindow):
  def __init__(self, parent=None):
    QMainWindow.__init__(self, parent)

    self.mem_dock = MemoryDockWidget(self)
    # dock areas really would be Left and Right :)
    self.addDockWidget(Qt.RightDockWidgetArea, self.mem_dock)

    self.cpu_dock = CPUDockWidget(self)
    # dock areas really would be Left and Right :)
    self.addDockWidget(Qt.LeftDockWidgetArea, self.cpu_dock)

    self.dev_dock = DevDockWidget(self)
    # dock areas really would be Left and Right :)
    self.addDockWidget(Qt.RightDockWidgetArea, self.dev_dock)

    self.setAttribute(Qt.WA_DeleteOnClose)
    self.setupUi(self)

    self.file_filters = self.tr("MIX source files (*.mix);;All files (*.*)");
    self.slot_File_New()

    self.errors_list.setBuddyText(self.txt_source)

    self.connect_all()

    self.connect(self.action_Quit, SIGNAL("triggered()"), qApp, SLOT("closeAllWindows()"))
    self.connect(self.txt_source, SIGNAL("textChanged()"), lambda: self.setWindowModified(True))

    self.connect(self.action_Open, SIGNAL("triggered()"), self.slot_File_Open)
    self.connect(self.action_New, SIGNAL("triggered()"), self.slot_File_New)
    self.connect(self.action_Save, SIGNAL("triggered()"), self.slot_File_Save)
    self.connect(self.action_Save_as, SIGNAL("triggered()"), self.slot_File_SaveAs)

    self.connect(self.action_Assemble, SIGNAL("triggered()"), self.slot_Assemble)
    self.connect(self.action_Step, SIGNAL("triggered()"), self.slot_Step)
    self.connect(self.action_Trace, SIGNAL("triggered()"), self.slot_Trace)
    self.connect(self.action_Run, SIGNAL("triggered()"), self.slot_Run)
    self.connect(self.action_Break, SIGNAL("triggered()"), self.slot_Break)

    self.connect(self.action_Change_font, SIGNAL("triggered()"), self.slot_Change_font)

    about_text = self.tr("""
    <h2>Mix Machine</h2><br><br>
    An implementation of Don Knuth's MIX machine in Python with GUI<br>
    Project's homepage - <a href="http://github.com/be9/mix-machine">http://github.com/be9/mix-machine</a>
    """)
    self.connect(self.action_About_Mix_Machine, SIGNAL("triggered()"), lambda: QMessageBox.about(self, self.tr("About Mix Machine"), about_text))
    self.connect(self.action_About_Qt, SIGNAL("triggered()"), qApp, SLOT("aboutQt()"))

    self.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self.slot_cur_tab_changed)

    self.emit(SIGNAL("inited()"))

    self.output_device = QTextEditOutputDevice(
        mode = "w", block_size = 24 * 5, lock_time = 24*2, text_edit = self.dev_dock.text_printer
    )
    self.input_device = QTextEditInputDevice(
        mode = "r", block_size = 14 * 5, lock_time = 14*2, text_edit = self.dev_dock.text_terminal
    )

  def slot_cur_tab_changed(self, index):
    if index == 0:
      self.emit(SIGNAL("sourceTabFocused()"))
    else:
      self.emit(SIGNAL("traceTabFocused()"))

  def slot_Change_font(self):
    new_font, ok = QFontDialog.getFont(self.txt_source.font())
    if ok:
      self.emit(SIGNAL("fontChanged(QFont)"), new_font)

  def slot_File_New(self):
    if not self.checkUnsaved(): 
      return

    self.txt_source.setPlainText(u"")

    self.setWindowModified(False)

    self.setCurrentFile("")

    self.emit(SIGNAL("setNewSource()"))

    self.statusBar().showMessage(self.tr("Empty source file has been created."), 2000);

  def checkUnsaved(self):
    if not self.isWindowModified():
      return True

    button = QMessageBox.information(self, PROGRAM_NAME, \
        self.tr("Document was changed!"), \
        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

    if button == QMessageBox.Save:
      self.slot_File_Save()
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

      base, ext = os.path.splitext(unicode(fn))
      if ext == '' or ext == '.':
        fn = base + '.mix'

      if self.saveToFile(fn):
        self.setCurrentFile(fn)

  def closeEvent(self, ce):
    self.slot_Break() # break machine if running
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
      self.emit(SIGNAL("setNewSource()"))

      self.setCurrentFile(filename)

  def cpu_hook(self, item, old, new):
    self.cpu_dock.hook(item, old, new)
    self.listing_view.hook(item, old, new)
    self.disasm_view.hook(item, old, new)

  def mem_hook(self, addr, old, new):
    self.mem_dock.hook(addr, old, new)
    self.listing_view.hook(addr, old, new)
    self.disasm_view.hook(addr, old, new)

  def lock_hook(self, mode, old, new):
    self.mem_dock.hook(mode, old, new)
    self.listing_view.hook(mode, old, new)
    self.disasm_view.hook(mode, old, new)

  def slot_Assemble(self):
    ret_type, content = asm(unicode(self.txt_source.toPlainText()))
    if ret_type == ASM_NO_ERRORS:
      self.asm_data = content # mem, start_addr, listing
      self.vm_data = VMData(self.asm_data) # vm, listing

      # add printer
      self.output_device.reset()
      self.vm_data.addDevice(18, self.output_device)
      # add input terminal
      self.input_device.reset()
      self.vm_data.addDevice(19, self.input_device)

      self.emit(SIGNAL("assembleSuccess(PyQt_PyObject, PyQt_PyObject)"), self.vm_data, self.asm_data)
      return

    # we have errors! (emit type of errors and list of errors)
    self.emit(SIGNAL("assembleGotErrors(int, QStringList)"), ret_type, [ "%i: %s" % err for err in content ])

  def enableHooks(self, enable = True):
    if enable:
      self.vm_data.setCPUHook(self.cpu_hook)
      self.vm_data.setMemHook(self.mem_hook)
      self.vm_data.setLockHook(self.lock_hook)
    else:
      self.vm_data.setCPUHook(None)
      self.vm_data.setMemHook(None)
      self.vm_data.setLockHook(None)

  def start_action(self):
    self.running = True
    #self.emit(SIGNAL("startedAction()")) # not used

  def stop_action(self):
    self.running = False
    self.emit(SIGNAL("stoppedAction()"))

  def doAction(self, action):
    if self.vm_data.halted():
      QMessageBox.information(self, self.tr("Mix machine"), self.tr("Mix machine is halted."))
      return

    try:
      self.start_action()
      action()
    except Exception, err:
      self.stop_action()
      if err in self.vm_data.vm_errors:
        QMessageBox.critical(self, self.tr("Runtime error"), str(err))
      else:
        raise err
    else:
      self.stop_action()
      if self.vm_data.halted():
        QMessageBox.information(self, self.tr("Mix machine"), self.tr("Mix machine was halted."))

  def slot_Step(self):
    self.emit(SIGNAL("beforeTrace()"))
    self.doAction(self.vm_data.step)
    self.emit(SIGNAL("afterTrace()"))

  def trace_vm(self):
    while not self.vm_data.halted() and self.running:
      self.cpu_dock.resetHighlight() # it's necessary
      self.vm_data.step()
      QCoreApplication.processEvents()
      if self.vm_data.ca() in self.breaks:
        break

  def run_vm(self):
    while not self.vm_data.halted() and self.running:
      self.vm_data.step()
      QCoreApplication.processEvents()
      if self.vm_data.ca() in self.breaks:
        break

  def slot_Trace(self):
    self.emit(SIGNAL("beforeTrace()"))
    self.doAction(self.trace_vm)
    self.emit(SIGNAL("afterTrace()"))

  def slot_Run(self):
    self.emit(SIGNAL("beforeRun()"))

    self.progress = QProgressDialog(self.tr("Running (%1 cycles passed)").arg(0), self.tr("Break run"), 0, 10, self)
    self.progress.setMinimumDuration(0)
    self.progress.setAutoClose(False)
    self.progress.setAutoReset(False)
    self.connect(self.progress, SIGNAL("canceled()"), self.slot_Break)

    self.progress_timer = QTimer(self)
    self.connect(self.progress_timer, SIGNAL("timeout()"), self.progressTick)
    self.connect(self, SIGNAL("stoppedAction()"), self.progress_timer, SLOT("stop()"))
    self.progress_timer.start(100)

    self.progress.setValue(0)
    self.doAction(self.run_vm)

    self.progress_timer.stop()
    self.progress.cancel()
    del self.progress, self.progress_timer

    self.emit(SIGNAL("afterRun(PyQt_PyObject)"), self.vm_data)

  def progressTick(self):
    self.progress.setLabelText(self.tr("Running (%1 cycles passed)").arg(self.vm_data.cycles()))
    if self.progress.value() == self.progress.maximum():
      self.progress.setValue(0)
    else:
      self.progress.setValue(self.progress.value() + 1)

  def slot_Break(self):
    self.emit(SIGNAL("breaked()"))
    self.running = False

  def resetBreakpointSet(self):
    self.breaks = set()
    self.listing_view.setBreakpointSet(self.breaks)
    self.disasm_view.setBreakpointSet(self.breaks)

  # menubar slots
  def menuBarHideRun(self):
    self.menu_File.setEnabled(        True)
    self.menu_Options.setEnabled(     True)
    self.action_Assemble.setEnabled(  True)
    self.action_Step.setEnabled(      False)
    self.action_Trace.setEnabled(     False)
    self.action_Run.setEnabled(       False)
    self.action_Break.setEnabled(     False)
  def menuBarShowRun(self):
    self.menu_File.setEnabled(        True)
    self.menu_Options.setEnabled(     True)
    self.action_Assemble.setEnabled(  True)
    self.action_Step.setEnabled(      True)
    self.action_Trace.setEnabled(     True)
    self.action_Run.setEnabled(       True)
    self.action_Break.setEnabled(     False)
  def menuBarShowBreak(self):
    self.menu_File.setEnabled(        False)
    self.menu_Options.setEnabled(     False)
    self.action_Assemble.setEnabled(  False)
    self.action_Step.setEnabled(      False)
    self.action_Trace.setEnabled(     False)
    self.action_Run.setEnabled(       False)
    self.action_Break.setEnabled(     True)

  def connect_all(self):
    # errors_list
    self.connect(self, SIGNAL("inited()"),                                        self.errors_list.hide)
    self.connect(self, SIGNAL("setNewSource()"),                                  self.errors_list.hide)
    self.connect(self, SIGNAL("assembleSuccess(PyQt_PyObject, PyQt_PyObject)"),   self.errors_list.hide)
    self.connect(self, SIGNAL("assembleGotErrors(int, QStringList)"),             self.errors_list.setErrors)

    # menubar
    self.connect(self, SIGNAL("inited()"),                                        self.menuBarHideRun)
    self.connect(self, SIGNAL("setNewSource()"),                                  self.menuBarHideRun)
    self.connect(self, SIGNAL("assembleGotErrors(int, QStringList)"),             self.menuBarHideRun)
    self.connect(self, SIGNAL("assembleSuccess(PyQt_PyObject, PyQt_PyObject)"),   self.menuBarShowRun)
    self.connect(self, SIGNAL("afterTrace()"),                                    self.menuBarShowRun)
    self.connect(self, SIGNAL("afterRun(PyQt_PyObject)"),                         self.menuBarShowRun)
    self.connect(self, SIGNAL("beforeTrace()"),                                   self.menuBarShowBreak)
    self.connect(self, SIGNAL("beforeRun()"),                                     self.menuBarShowBreak)

    # tabs
    self.connect(self, SIGNAL("inited()"),                                        self.tabWidget.hideRun)
    self.connect(self, SIGNAL("setNewSource()"),                                  self.tabWidget.hideRun)
    self.connect(self, SIGNAL("assembleGotErrors(int, QStringList)"),             self.tabWidget.hideRun)
    self.connect(self, SIGNAL("assembleSuccess(PyQt_PyObject, PyQt_PyObject)"),   self.tabWidget.showRun)
    self.connect(self, SIGNAL("traceTabFocused()"),                               self.tabWidget.rememberRunTab)

    # enable and disable hooks
    self.connect(self, SIGNAL("beforeTrace()"),                           lambda: self.enableHooks(True))
    self.connect(self, SIGNAL("beforeRun()"),                             lambda: self.enableHooks(False))

    # txt_source
    self.connect(self, SIGNAL("fontChanged(QFont)"),                              self.txt_source.setFont)

    # listing and disassembler
    for widget in (self.listing_view, self.disasm_view):
      self.connect(self, SIGNAL("inited()"),                                      widget.init)
      self.connect(self, SIGNAL("fontChanged(QFont)"),                            widget.changeFont)
      self.connect(self, SIGNAL("assembleSuccess(PyQt_PyObject, PyQt_PyObject)"), widget.resetVM)
      self.connect(self, SIGNAL("beforeRun()"),                                   widget.snapshotMem)
      self.connect(self, SIGNAL("afterRun(PyQt_PyObject)"),                       widget.updateVM)

    # all trace widgets visibility
    for widget in (self.cpu_dock, self.mem_dock, self.dev_dock):
      self.connect(self, SIGNAL("inited()"),                                      widget.hide)
      self.connect(self, SIGNAL("sourceTabFocused()"),                            widget.hide)
      self.connect(self, SIGNAL("traceTabFocused()"),                             widget.show)

    # cpu_dock
    self.connect(self, SIGNAL("assembleSuccess(PyQt_PyObject, PyQt_PyObject)"),   self.cpu_dock.init)
    self.connect(self, SIGNAL("afterRun(PyQt_PyObject)"),                         self.cpu_dock.reload)
    self.connect(self, SIGNAL("beforeRun()"),                                     self.cpu_dock.resetHighlight)
    self.connect(self, SIGNAL("beforeTrace()"),                                   self.cpu_dock.resetHighlight)

    # mem_dock
    self.connect(self, SIGNAL("assembleSuccess(PyQt_PyObject, PyQt_PyObject)"),   self.mem_dock.init)
    self.connect(self, SIGNAL("afterRun(PyQt_PyObject)"),                         self.mem_dock.reload)

    self.connect(self, SIGNAL("setNewSource()"),                                  self.resetBreakpointSet)

if __name__ == "__main__":
  app = QApplication(sys.argv)

  mw = MainWindow()
  mw.show()
  sys.exit(app.exec_())
