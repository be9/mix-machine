from PyQt4.QtGui import *
from PyQt4.QtCore import *

from math import log10 # needed to calculate number of digits in Cycles counter

from word_edit import WordEdit
from mix_word_widget import *

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))

from word import *

registers = "a x i1 i2 i3 i4 i5 i6 j".split()
flags = "ca cf of hlt cycles".split()

HIGHLIGHT_STYLE = "MixWordWidget, QComboBox { background: gray }"

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
      self.__dict__["edit_" + s].setWord(self.vm_data.vm[s.upper()])
    for s in "i1 i2 i3 i4 i5 i6".split():
      self.__dict__["edit_" + s].setWord(self.vm_data.vm[s[1].upper()])
    self.edit_ca.setValue(self.vm_data.vm["cur_addr"])
    self.edit_cf.setCurrentIndex(self.vm_data.vm["cf"] + 1)
    self.edit_of.setCurrentIndex(int(self.vm_data.vm["of"]))
    self.edit_hlt.setCurrentIndex(int(self.vm_data.vm["halted"]))
    self.edit_cycles.display(self.vm_data.vm["cycles"])

  def highlight(self, object, flag):
    if not flag:
      object.setStyleSheet(u"")
    else:
      object.setStyleSheet(HIGHLIGHT_STYLE)

  def resetHighlight(self):
    map(lambda obj: self.highlight(obj, False), self.all_edits)

  def hook(self, item, old, new):
    # item - in UPPER
    if item == "cur_addr":
      self.edit_ca.setValue(new)

    elif item in "AXJ":
      self.__dict__["edit_" + item.lower()].setWord(new)
      self.highlight(self.__dict__["edit_" + item.lower()], True)

    elif item in "123456":
      self.__dict__["edit_i" + item].setWord(new)
      self.highlight(self.__dict__["edit_i" + item], True)

    elif item == "cf":
      self.edit_cf.setCurrentIndex(new + 1)
      self.highlight(self.edit_cf, True)

    elif item == "of":
      self.edit_of.setCurrentIndex(int(new))
      self.highlight(self.edit_of, True)

    elif item == "halted":
      self.edit_hlt.setCurrentIndex(int(new))
      self.highlight(self.edit_hlt, True)

    elif item == "cycles":
      self.edit_cycles.display(new)

  def setVM(self, what, value = None):
    # what - in lower
    if what in "axj":
      if value is None:
        self.vm_data.vm[what.upper()] = Word(self.__dict__["edit_"+what].word)
      else:
        self.vm_data.vm[what.upper()] = Word(value)

    elif what in "i1 i2 i3 i4 i5 i6".split():
      if value is None:
        self.vm_data.vm[what[1]] = Word(self.__dict__["edit_"+what].word)
      else:
        self.vm_data.vm[what[1]] = Word(value)

    elif what == "ca":
      self.vm_data.vm["cur_addr"] = value

    elif what == "cf":
      self.vm_data.vm["cf"] = value - 1

    elif what == "of":
      self.vm_data.vm["of"] = bool(value)

    elif what == "hlt":
      self.vm_data.vm["halted"] = bool(value)

  def slot_cycles_overflow(self):
    # log10(cycles.value()) rounded up - this is number of digits :) (learn math)
    self.edit_cycles.setNumDigits(int(log10(self.edit_cycles.intValue()))+1)
    self.edit_cycles.display(self.edit_cycles.intValue())

  def initConnections(self):
    # this DOESN'T work!!! (it seems like all changes are made in rJ)
    #for s in registers:
      #self.connect(self.__dict__["edit_"+s], SIGNAL("valueChanged()"),\
        #lambda: self.setVM(s))
    # this DOESN'T work!!! (it seems like all changes are made in hlt)
    #for s in "cf of hlt".split():
      #self.connect(self.__dict__["edit_"+s], SIGNAL("currentIndexChanged(int)"),\
        #lambda index: self.setVM(s, index))
    self.connect(self.edit_a, SIGNAL("valueChanged()"),             lambda: self.setVM("a"))
    self.connect(self.edit_x, SIGNAL("valueChanged()"),             lambda: self.setVM("x"))
    self.connect(self.edit_j, SIGNAL("valueChanged()"),             lambda: self.setVM("j"))
    self.connect(self.edit_i1, SIGNAL("valueChanged()"),            lambda: self.setVM("i1"))
    self.connect(self.edit_i2, SIGNAL("valueChanged()"),            lambda: self.setVM("i2"))
    self.connect(self.edit_i3, SIGNAL("valueChanged()"),            lambda: self.setVM("i3"))
    self.connect(self.edit_i4, SIGNAL("valueChanged()"),            lambda: self.setVM("i4"))
    self.connect(self.edit_i5, SIGNAL("valueChanged()"),            lambda: self.setVM("i5"))
    self.connect(self.edit_i6, SIGNAL("valueChanged()"),            lambda: self.setVM("i6"))
    self.connect(self.edit_ca, SIGNAL("valueChanged(int)"),         lambda i: self.setVM("ca", i))
    self.connect(self.edit_cf, SIGNAL("currentIndexChanged(int)"),  lambda index: self.setVM("cf", index))
    self.connect(self.edit_of, SIGNAL("currentIndexChanged(int)"),  lambda index: self.setVM("of", index))
    self.connect(self.edit_hlt, SIGNAL("currentIndexChanged(int)"), lambda index: self.setVM("hlt", index))

  def initWidgets(self):
    self.setWindowTitle(self.tr("CPU"))

    self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)

    self.widget = QWidget()

    # it will be need in resetHighlight
    self.all_edits = []

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
      self.all_edits.append(edit)

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
    #self.all_edits.append(self.edit_ca) # no highlight

    self.edit_cf = QComboBox(self)
    self.edit_cf.setObjectName("edit_cf")
    self.edit_cf.addItems([
      self.tr("Less"),
      self.tr("Equal"),
      self.tr("Greater")
    ])
    self.edit_cf.setCurrentIndex(1)
    self.all_edits.append(self.edit_cf)

    self.edit_of = QComboBox(self)
    self.edit_of.setObjectName("edit_of")
    self.edit_of.addItems([
      self.tr("False"),
      self.tr("True")
    ])
    self.edit_of.setCurrentIndex(0)
    self.all_edits.append(self.edit_of)

    self.edit_hlt = QComboBox(self)
    self.edit_hlt.setObjectName("edit_hlt")
    self.edit_hlt.addItems([
      self.tr("False"),
      self.tr("True")
    ])
    self.edit_hlt.setCurrentIndex(0)
    self.all_edits.append(self.edit_hlt)

    self.edit_cycles = QLCDNumber(self)
    self.edit_cycles.setObjectName("edit_cycles")
    self.edit_cycles.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
    self.edit_cycles.setSegmentStyle(QLCDNumber.Flat)
    #self.all_edits.append(self.edit_cycles) # not edited (readonly)
    self.connect(self.edit_cycles, SIGNAL("overflow()"), self.slot_cycles_overflow)

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