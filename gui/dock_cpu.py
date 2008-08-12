from PyQt4.QtGui import *
from PyQt4.QtCore import *

from cell_edit import CellEdit
from mix_word_widget import MixWordWidget

import gui_vm

registers = "a x i1 i2 i3 i4 i5 i6 j".split()
flags = "ca cf of hlt cycles".split()

class CPUDockWidget(QDockWidget):
  def __init__(self, parent = None):
    QDockWidget.__init__(self, parent)
    self.initWidgets()

  def setVMData(self, vm_data):
    self.edit_ca.setMaximum(vm_data.vm.MEMORY_SIZE)
    self.vm_data = vm_data

  def loadFromVM(self):
    for s in "a x j".split():
      self.__dict__["edit_" + s].setText(str(self.vm_data.vm.__dict__["r" + s.upper()]))
    for s in "i1 i2 i3 i4 i5 i6".split():
      self.__dict__["edit_" + s].setText(str(self.vm_data.vm.__dict__["r" + s[1:].upper()]))
    self.edit_ca.setValue(self.vm_data.vm.cur_addr)
    self.edit_cf.setCurrentIndex(self.vm_data.vm.cf + 1)
    self.edit_of.setCurrentIndex(int(self.vm_data.vm.of))
    self.edit_hlt.setCurrentIndex(int(self.vm_data.vm.halted))
    self.edit_cycles.display(self.vm_data.vm.cycles)

  def initConnections(self):
    pass


  def initWidgets(self):
    self.setWindowTitle(self.tr("CPU"))

    self.widget = QWidget()

    # create box for registers
    self.registers = QGroupBox(self)
    self.reg_layout = QGridLayout()

    # create and lay all registers
    current_row_in_grid = 0
    for reg in registers:
      label   = self.__dict__["label_" + reg]   = QLabel("r" + reg.upper(), self.registers)
      edit    = self.__dict__["edit_" + reg]    = MixWordWidget(self.registers)

      label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

      self.reg_layout.addWidget(label,  current_row_in_grid, 0)
      self.reg_layout.addWidget(edit,   current_row_in_grid, 1)
      current_row_in_grid += 1

    self.registers.setLayout(self.reg_layout)

    # create all flags:
    # first create all labels
    for flag in flags:
      label = self.__dict__["label_" + flag]   = QLabel(self.tr(flag.upper()), self)
      label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    # than create edit-widgets
    self.edit_ca = QSpinBox(self)
    self.edit_ca.setMinimum(0)
    #self.edit_ca.setMaximum(0) # it will be set in setVMData

    self.edit_cf = QComboBox(self)
    self.edit_cf.addItems([
      self.tr("Less"),
      self.tr("Equal"),
      self.tr("Greater")
    ])
    self.edit_cf.setCurrentIndex(1)

    self.edit_of = QComboBox(self)
    self.edit_of.addItems([
      self.tr("False"),
      self.tr("True")
    ])
    self.edit_of.setCurrentIndex(0)

    self.edit_hlt = QComboBox(self)
    self.edit_hlt.addItems([
      self.tr("False"),
      self.tr("True")
    ])
    self.edit_hlt.setCurrentIndex(0)

    self.edit_cycles = QLCDNumber(self)
    self.edit_cycles.setSegmentStyle(QLCDNumber.Flat)

    # add box with registers to main_layout
    self.main_layout = QGridLayout()
    self.main_layout.addWidget(self.registers, 0, 0, 1, 4)

    # add all flags to main_layout
    current_row_in_grid = 1
    for flag in flags:
      self.main_layout.addWidget(self.__dict__["label_" + flag],  current_row_in_grid, 0, 1, 1)
      self.main_layout.addWidget(self.__dict__["edit_" + flag],   current_row_in_grid, 1, 1, 3)
      current_row_in_grid += 1

    self.widget.setLayout(self.main_layout)
    self.setWidget(self.widget)

if __name__ == "__main__":
  import sys
  app = QApplication(sys.argv)

  dock = CPUDockWidget(None)
  dock.show()

  sys.exit(app.exec_())