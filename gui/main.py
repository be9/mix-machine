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
from listing_model import ListingModel
from disasm_model import DisassemblerModel

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
    self.setCurrentFile("")

    self.txt_source.setPlainText(u"")

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

    self.connect(self.errors_list, SIGNAL("itemDoubleClicked(QListWidgetItem *)"),
        self.slot_clickOnError)

    self.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self.slot_cur_tab_changed)

    self.setRunWidgetsEnabled(False)
    self.errors_list.setVisible(False)

    # init listing and disasmmler view
    self.listing_model = ListingModel(parent = self)
    self.listing_view.setModel(self.listing_model) # add model to set size of header
    self.listing_view.horizontalHeader().setStretchLastSection(True) # for column with source line
    self.listing_view.setSelectionMode(QAbstractItemView.NoSelection)

    self.disasm_model = DisassemblerModel(parent = self)
    self.disasm_view.setModel(self.disasm_model) # add model to set size of header
    self.disasm_view.horizontalHeader().setStretchLastSection(True) # for column with disasm line
    self.disasm_view.setSelectionMode(QAbstractItemView.NoSelection)

    self.resetSizes()

    self.slot_cur_tab_changed(0)

    self.output_device = QTextEditOutputDevice(
        mode = "w", block_size = 24 * 5, lock_time = 24*2, text_edit = self.dev_dock.text_printer
    )
    self.input_device = QTextEditInputDevice(
        mode = "r", block_size = 14 * 5, lock_time = 14*2, text_edit = self.dev_dock.text_terminal
    )

  def slot_cur_tab_changed(self, index):
    visible = index != 0 # hide dock widgets at source editing tab
    self.mem_dock.setVisible(visible)
    self.cpu_dock.setVisible(visible)
    self.dev_dock.setVisible(visible)
    if visible:
      self.listing_and_disasm_goto_ca()

  def resetSizes(self):
    """Call after font changes"""
    font_metrics = QFontMetrics(self.listing_view.font())
    addr = font_metrics.width("0000")
    word = font_metrics.width("+ 00 00 00 00 00")

    h_header = self.listing_view.horizontalHeader()
    h_header.setStretchLastSection(True) # for column with source line
    h_header.resizeSection(h_header.logicalIndex(0), addr + 20)
    h_header.resizeSection(h_header.logicalIndex(1), word + 20)

    h_header = self.disasm_view.horizontalHeader()
    h_header.setStretchLastSection(True) # for column with disasm line
    h_header.resizeSection(h_header.logicalIndex(0), addr + 20)
    h_header.resizeSection(h_header.logicalIndex(1), word + 20)

  def slot_Change_font(self):
    new_font, ok = QFontDialog.getFont(self.txt_source.font())
    if ok:
      self.txt_source.setFont(new_font)
      self.listing_view.setFont(new_font)
      self.resetSizes()

  def setRunWidgetsEnabled(self, enable):
    self.tabWidget.setTabEnabled(1, enable)
    self.tabWidget.setTabEnabled(2, enable)
    self.action_Step.setEnabled(enable)
    self.action_Trace.setEnabled(enable)
    self.action_Run.setEnabled(enable)
    self.action_Break.setEnabled(enable)

  def setBreakEnabledOnly(self, enable):
    self.menu_File.setEnabled(not enable)
    self.menu_Options.setEnabled(not enable)
    self.action_Assemble.setEnabled(not enable)
    self.action_Step.setEnabled(not enable)
    self.action_Trace.setEnabled(not enable)
    self.action_Run.setEnabled(not enable)
    self.action_Break.setEnabled(enable)

  def setNewSource(self):
    self.setRunWidgetsEnabled(False)
    self.tabWidget.setCurrentIndex(0)
    self.errors_list.setVisible(False)

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
    self.slot_Break()
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
      self.setNewSource()

      self.setCurrentFile(filename)

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

  def cpu_hook(self, item, old, new):
    self.cpu_dock.hook(item, old, new)
    self.listing_model.hook(item, old, new)
    self.disasm_model.hook(item, old, new)
    if item == "cur_addr":
      self.listing_and_disasm_goto_ca()

  def mem_hook(self, addr, old, new):
    self.mem_dock.hook(addr, old, new)
    self.listing_model.hook(addr, old, new)
    self.disasm_model.hook(addr, old, new)

  def lock_hook(self, mode, old, new):
    self.mem_dock.hook(mode, old, new)
    self.listing_model.hook(mode, old, new)
    self.disasm_model.hook(mode, old, new)

  def resetListingAndDisasm(self):
    self.listing_model = ListingModel(vm_data = self.vm_data, parent = self)
    self.listing_view.setModel(self.listing_model)

    self.disasm_model = DisassemblerModel(vm_data = self.vm_data, asm_data = self.asm_data, parent = self)
    self.disasm_view.setModel(self.disasm_model)

    self.listing_and_disasm_goto_ca()

  def slot_Assemble(self):
    self.errors_list.setVisible(False)
    self.setRunWidgetsEnabled(False)
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

      self.mem_dock.initModel(self.vm_data)

      self.cpu_dock.setVMData(self.vm_data)
      self.cpu_dock.loadFromVM()
      self.cpu_dock.resetHighlight()

      self.resetListingAndDisasm()

      self.setRunWidgetsEnabled(True)
      self.setBreakEnabledOnly(False)
      self.tabWidget.setCurrentIndex(1)
      self.statusBar().showMessage(self.tr("Source assembled and virtual machine initialized"), 2000)
      return

    # we have errors!
    if ret_type == ASM_SYNTAX_ERRORS:
      err_mesg = self.tr("There are syntax errors")
    else:
      err_mesg = self.tr("There are assemble errors")

    # content - errors
    self.errors_list.clear()
    self.errors_list.addItems([ "%i: %s" % err for err in content ])
    self.errors_list.setVisible(True)

    self.statusBar().showMessage(err_mesg, 2000)

  def enableHooks(self, enable = True):
    if enable:
      self.vm_data.setCPUHook(self.cpu_hook)
      self.vm_data.setMemHook(self.mem_hook)
      self.vm_data.setLockHook(self.lock_hook)
    else:
      self.vm_data.setCPUHook(None)
      self.vm_data.setMemHook(None)
      self.vm_data.setLockHook(None)

  def doVMAction(self, action):
    self.breaked = False
    if self.vm_data.halted():
      QMessageBox.information(self, self.tr("Mix machine"), self.tr("Mix machine is halted."))
      return

    self.cpu_dock.resetHighlight()
    self.setBreakEnabledOnly(True)
    try:
      action()
    except Exception, err:
      QMessageBox.critical(self, self.tr("Runtime error"), str(err))
    else:
      self.listing_and_disasm_goto_ca()
      if self.vm_data.halted():
        QMessageBox.information(self, self.tr("Mix machine"), self.tr("Mix machine was halted."))
    self.setBreakEnabledOnly(False)

  def slot_Step(self):
    self.enableHooks()
    self.doVMAction(self.vm_data.step)

  def run_vm(self):
    while not self.vm_data.halted() and not self.breaked:
      self.vm_data.step()
      QCoreApplication.processEvents()

  def slot_Trace(self):
    self.enableHooks()
    self.doVMAction(self.run_vm)

  def enableAllWidgetsButDev(self, enable):
    self.tabWidget.setEnabled(enable)
    self.cpu_dock.setEnabled(enable)
    self.mem_dock.setEnabled(enable)

  def slot_Run(self):
    self.enableHooks(False)
    self.enableAllWidgetsButDev(False)

    self.progress = QProgressDialog(self.tr("Running (%1 cycles passed)").arg(0), self.tr("Break run"), 0, 10, self)
    self.progress.setMinimumDuration(1000)
    self.progress.setAutoClose(False)
    self.progress.setAutoReset(False)
    self.connect(self.progress, SIGNAL("canceled()"), self.slot_Break)

    self.progress_timer = QTimer(self)
    self.connect(self.progress_timer, SIGNAL("timeout()"), self.progressTick)
    self.progress_timer.start(1000)

    self.progress.setValue(0)
    self.doVMAction(self.run_vm)

    self.progress_timer.stop()
    self.progress.cancel()
    del self.progress, self.progress_timer

    self.enableAllWidgetsButDev(True)
    self.cpu_dock.loadFromVM()
    self.resetListingAndDisasm()

  def progressTick(self):
    self.progress.setLabelText(self.tr("Running (%1 cycles passed)").arg(self.vm_data.cycles()))
    if self.progress.value() == self.progress.maximum():
      self.progress.setValue(0)
    else:
      self.progress.setValue(self.progress.value() + 1)

  def listing_and_disasm_goto_ca(self):
    """Selects row near ca"""
    if self.tabWidget.currentIndex() == 1: # listing
      num = self.listing_model.current_line
      if num is None:
          self.statusBar().showMessage(self.tr("Mix machine's current address is out of listing."))
      else:
        self.listing_view.setCurrentIndex(self.listing_model.index(num, 0))
    elif self.tabWidget.currentIndex() == 2: # disasm
      self.disasm_view.setCurrentIndex(self.disasm_model.index(self.disasm_model.ca, 0))

  def slot_Break(self):
    self.breaked = True

if __name__ == "__main__":
  app = QApplication(sys.argv)

  mw = MainWindow()
  mw.show()
  sys.exit(app.exec_())
