from PyQt4.QtGui import *
from PyQt4.QtCore import *

from math import log10 # needed to calculate number of digits in Cycles counter

from word_edit import WordEdit
from mix_word_widget import *

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))

from word import *

registers = "ax123456j"
flags = "cur_addr cf of halted cycles".split()
label_flags = "CA CF OF HLT CyCLES".split()

HIGHLIGHT_STYLE = "MixWordWidget, QComboBox { background: gray }"

class CPUDockWidget(QDockWidget):
  def __init__(self, parent = None):
    QDockWidget.__init__(self, parent)
    self.initWidgets()
    self.initConnections()

  def init(self, vm_data):
    self.edit_cur_addr.setMaximum(vm_data.vm.MEMORY_SIZE - 1)
    self.vm_data = vm_data
    self.reload()
    self.resetHighlight()

  def reload(self):
    for s in registers.upper():
      self.setItem(s, self.vm_data.vm[s])
    for s in flags:
      self.setItem(s, self.vm_data.vm[s])

  def highlight(self, object, flag = True):
    if not flag:
      object.setStyleSheet(u"")
    else:
      object.setStyleSheet(HIGHLIGHT_STYLE)

  def resetHighlight(self):
    map(lambda obj: self.highlight(obj, False), self.all_edits)

  def setItem(self, item, value):
    item = item.lower()
    if item == "cur_addr":
      self.edit_cur_addr.setValue(value)
    elif item in registers:
      self.__dict__["edit_" + item.lower()].setWord(value)
    elif item == "cf":
      self.edit_cf.setCurrentIndex(value + 1)
    elif item == "of":
      self.edit_of.setCurrentIndex(int(value))
    elif item == "halted":
      self.edit_halted.setCurrentIndex(int(value))
    elif item == "cycles":
      self.edit_cycles.display(value)

  def hook(self, item, old, new):
    self.setItem(item, new)

  def setVM(self, what, value = None):
    what = what.lower()
    if what in registers:
      if value is None:
        self.vm_data.vm[what.upper()] = Word(self.__dict__["edit_"+what].word)
      else:
        self.vm_data.vm[what.upper()] = Word(value)
    elif what == "cur_addr":
      self.vm_data.vm["cur_addr"] = value
    elif what == "cf":
      self.vm_data.vm["cf"] = value - 1
    elif what in ("of", "halted"):
      self.vm_data.vm[what] = bool(value)

  def slot_cycles_overflow(self):
    # log10(cycles.value()) rounded up - this is number of digits :) (learn math)
    self.edit_cycles.setNumDigits(int(log10(self.edit_cycles.intValue()))+1)
    self.edit_cycles.display(self.edit_cycles.intValue())

  def initConnections(self):
    self.connect(self.edit_a, SIGNAL("valueChanged()"),                 lambda: self.setVM("a"))
    self.connect(self.edit_x, SIGNAL("valueChanged()"),                 lambda: self.setVM("x"))
    self.connect(self.edit_j, SIGNAL("valueChanged()"),                 lambda: self.setVM("j"))
    self.connect(self.edit_1, SIGNAL("valueChanged()"),                 lambda: self.setVM("1"))
    self.connect(self.edit_2, SIGNAL("valueChanged()"),                 lambda: self.setVM("2"))
    self.connect(self.edit_3, SIGNAL("valueChanged()"),                 lambda: self.setVM("3"))
    self.connect(self.edit_4, SIGNAL("valueChanged()"),                 lambda: self.setVM("4"))
    self.connect(self.edit_5, SIGNAL("valueChanged()"),                 lambda: self.setVM("5"))
    self.connect(self.edit_6, SIGNAL("valueChanged()"),                 lambda: self.setVM("6"))
    self.connect(self.edit_cur_addr, SIGNAL("valueChanged(int)"),       lambda i: self.setVM("cur_addr", i))
    self.connect(self.edit_cf, SIGNAL("currentIndexChanged(int)"),      lambda index: self.setVM("cf", index))
    self.connect(self.edit_of, SIGNAL("currentIndexChanged(int)"),      lambda index: self.setVM("of", index))
    self.connect(self.edit_halted, SIGNAL("currentIndexChanged(int)"),  lambda index: self.setVM("hlt", index))

    self.connect(self.edit_a, SIGNAL("valueChanged()"),                 lambda: self.highlight(self.edit_a))
    self.connect(self.edit_x, SIGNAL("valueChanged()"),                 lambda: self.highlight(self.edit_x))
    self.connect(self.edit_j, SIGNAL("valueChanged()"),                 lambda: self.highlight(self.edit_j))
    self.connect(self.edit_1, SIGNAL("valueChanged()"),                 lambda: self.highlight(self.edit_1))
    self.connect(self.edit_2, SIGNAL("valueChanged()"),                 lambda: self.highlight(self.edit_2))
    self.connect(self.edit_3, SIGNAL("valueChanged()"),                 lambda: self.highlight(self.edit_3))
    self.connect(self.edit_4, SIGNAL("valueChanged()"),                 lambda: self.highlight(self.edit_4))
    self.connect(self.edit_5, SIGNAL("valueChanged()"),                 lambda: self.highlight(self.edit_5))
    self.connect(self.edit_6, SIGNAL("valueChanged()"),                 lambda: self.highlight(self.edit_6))
    self.connect(self.edit_cf, SIGNAL("currentIndexChanged(int)"),      lambda: self.highlight(self.edit_cf))
    self.connect(self.edit_of, SIGNAL("currentIndexChanged(int)"),      lambda: self.highlight(self.edit_of))
    self.connect(self.edit_halted, SIGNAL("currentIndexChanged(int)"),  lambda: self.highlight(self.edit_halted))

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
    for i in xrange(len(flags)):
      label = self.__dict__["label_" + flags[i]]   = QLabel(self.tr(label_flags[i]), self)
      label.setObjectName("label_" + flags[i])
      label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    # than create edit-widgets
    self.edit_cur_addr = QSpinBox(self)
    self.edit_cur_addr.setObjectName("edit_cur_addr")
    self.edit_cur_addr.setMinimum(0)
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

    self.edit_halted = QComboBox(self)
    self.edit_halted.setObjectName("edit_halted")
    self.edit_halted.addItems([
      self.tr("False"),
      self.tr("True")
    ])
    self.edit_halted.setCurrentIndex(0)
    self.all_edits.append(self.edit_halted)

    self.edit_cycles = QLCDNumber(self)
    self.edit_cycles.setObjectName("edit_cycles")
    self.edit_cycles.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
    self.edit_cycles.setSegmentStyle(QLCDNumber.Flat)
    #self.all_edits.append(self.edit_cycles) # not edited (readonly)
    self.connect(self.edit_cycles, SIGNAL("overflow()"), self.slot_cycles_overflow)

    # add box with registers to main_layout
    self.main_layout = QGridLayout()

    # add all flags to main_layout
    for s in list(registers) + flags:
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