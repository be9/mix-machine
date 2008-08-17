# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'word_edit.ui'
#
# Created: Mon Aug 18 03:56:08 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,218,114).size()).expandedTo(Dialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(Dialog)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.type_word = QtGui.QRadioButton(Dialog)
        self.type_word.setChecked(True)
        self.type_word.setObjectName("type_word")
        self.hboxlayout.addWidget(self.type_word)

        self.type_int = QtGui.QRadioButton(Dialog)
        self.type_int.setObjectName("type_int")
        self.hboxlayout.addWidget(self.type_int)

        self.type_str = QtGui.QRadioButton(Dialog)
        self.type_str.setObjectName("type_str")
        self.hboxlayout.addWidget(self.type_str)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.input_line = QtGui.QLineEdit(Dialog)
        self.input_line.setWindowModality(QtCore.Qt.WindowModal)
        self.input_line.setObjectName("input_line")
        self.vboxlayout.addWidget(self.input_line)

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setAutoFillBackground(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),Dialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Cell #0000", None, QtGui.QApplication.UnicodeUTF8))
        self.type_word.setText(QtGui.QApplication.translate("Dialog", "Mix word", None, QtGui.QApplication.UnicodeUTF8))
        self.type_int.setText(QtGui.QApplication.translate("Dialog", "Integer", None, QtGui.QApplication.UnicodeUTF8))
        self.type_str.setText(QtGui.QApplication.translate("Dialog", "Text", None, QtGui.QApplication.UnicodeUTF8))

