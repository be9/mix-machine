from PyQt4.QtGui import *
from PyQt4.QtCore import *

from word_edit import WordEdit
from mix_word_widget import *

import gui_vm

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))

from word import *

registers = "a x i1 i2 i3 i4 i5 i6 j".split()
flags = "ca cf of hlt cycles".split()

class CPUDockWidget(QDockWidget):
  def __init__(self, parent = None):
    QDockWidget.__init__(self, parent)
    self.initWidgets()
    self.initConnections()

  def setVMData(self, vm_data):
    self.edit_ca.setMaximum(vm_data.vm.MEMORY_SIZE - 1)
    self.vm_data = vm_data
    self.loadFromVM()

  def loadFromVM(self):
    for s in "a x j".split():
      self.__dict__["edit_" + s].setWord(self.vm_data.vm.__dict__["r" + s.upper()])
    for s in "i1 i2 i3 i4 i5 i6".split():
      self.__dict__["edit_" + s].setWord(self.vm_data.vm.__dict__["r" + s[1:].upper()])
    self.edit_ca.setValue(self.vm_data.vm.cur_addr)
    self.edit_cf.setCurrentIndex(self.vm_data.vm.cf + 1)
    self.edit_of.setCurrentIndex(int(self.vm_data.vm.of))
    self.edit_hlt.setCurrentIndex(int(self.vm_data.vm.halted))
    self.edit_cycles.display(self.vm_data.vm.cycles)

  def setVM(self, what, value = None):
    if what in "a x j".split():
      self.vm_data.vm.__dict__["r"+what.upper()] = Word(self.__dict__["edit_"+what].word)

    elif what in "i1 i2 i3 i4 i5 i6".split():
      self.vm_data.vm.__dict__["r"+what[1:].upper()] = Word(self.__dict__["edit_"+what].word)

    elif what == "ca":
      self.vm_data.vm.cur_addr = value
      self.emit(SIGNAL("caChanged()"))

    elif what == "cf":
      self.vm_data.vm.cf = value - 1

    elif what == "of":
      self.vm_data.vm.of = bool(value)

    elif what == "hlt":
      self.vm_data.vm.halted = bool(value)

  def initConnections(self):
    for s in registers:
      self.connect(self.__dict__["edit_"+s], SIGNAL("valueChanged()"),\
        lambda: self.setVM(s))
    self.connect(self.edit_ca, SIGNAL("valueChanged(int)"),\
      lambda i: self.setVM("ca", i))
    # this code doesn't work... :( [signal of any comboBox executes all slots]
    #for s in "cf of hlt".split():
      #self.connect(self.__dict__["edit_"+s], SIGNAL("currentIndexChanged(int)"),\
        #lambda index: self.setVM(s, index))
    self.connect(self.edit_cf, SIGNAL("currentIndexChanged(int)"),\
      lambda index: self.setVM("cf", index))
    self.connect(self.edit_of, SIGNAL("currentIndexChanged(int)"),\
      lambda index: self.setVM("of", index))
    self.connect(self.edit_hlt, SIGNAL("currentIndexChanged(int)"),\
      lambda index: self.setVM("hlt", index))

  def initWidgets(self):
    self.setWindowTitle(self.tr("CPU"))

    self.widget = QWidget()

    # create and lay all registers
    current_row_in_grid = 0
    for reg in registers:
      label   = self.__dict__["label_" + reg]   = QLabel("r" + reg.upper(), self)
      if reg in "ax":
        type = BASIC
      elif reg == "j":
        type = REGJ
      else:
        type = INDEX
      edit    = self.__dict__["edit_" + reg]    = MixWordWidget(self, type)

      label.setObjectName("label_" + reg)
      edit.setObjectName("edit_" + reg)

      label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
      edit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
      current_row_in_grid += 1

    # create all flags:
    # first create all labels
    for flag in flags:
      label = self.__dict__["label_" + flag]   = QLabel(self.tr(flag.upper()), self)
      label.setObjectName("label_" + flag)
      label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    # than create edit-widgets
    self.edit_ca = QSpinBox(self)
    self.edit_ca.setObjectName("edit_ca")
    self.edit_ca.setMinimum(0)
    #self.edit_ca.setMaximum(0) # it will be set in setVMData

    self.edit_cf = QComboBox(self)
    self.edit_cf.setObjectName("edit_cf")
    self.edit_cf.addItems([
      self.tr("Less"),
      self.tr("Equal"),
      self.tr("Greater")
    ])
    self.edit_cf.setCurrentIndex(1)

    self.edit_of = QComboBox(self)
    self.edit_of.setObjectName("edit_of")
    self.edit_of.addItems([
      self.tr("False"),
      self.tr("True")
    ])
    self.edit_of.setCurrentIndex(0)

    self.edit_hlt = QComboBox(self)
    self.edit_hlt.setObjectName("edit_hlt")
    self.edit_hlt.addItems([
      self.tr("False"),
      self.tr("True")
    ])
    self.edit_hlt.setCurrentIndex(0)

    self.edit_cycles = QLCDNumber(self)
    self.edit_cycles.setObjectName("edit_cycles")
    self.edit_cycles.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
    self.edit_cycles.setSegmentStyle(QLCDNumber.Flat)

    # add box with registers to main_layout
    self.main_layout = QGridLayout()

    # add all flags to main_layout
    for s in registers + flags:
      self.main_layout.addWidget(self.__dict__["label_" + s],  current_row_in_grid, 0, 1, 1)
      self.main_layout.addWidget(self.__dict__["edit_" + s],   current_row_in_grid, 1, 1, 3)
      current_row_in_grid += 1

    self.widget.setLayout(self.main_layout)
    self.setWidget(self.widget)

if __name__ == "__main__":
  import sys
  app = QApplication(sys.argv)

  dock = CPUDockWidget(None)
  dock.show()

  sys.exit(app.exec_())