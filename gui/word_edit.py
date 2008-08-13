from PyQt4.QtCore import *
from PyQt4.QtGui import *

from cell_edit_ui import Ui_Dialog

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm2'))
from word import *
from device import *

# types
WORD  = 0
INT   = 1
STR   = 2

# content types
BASIC = 0
INDEX = 1
REGJ  = 2

def word2toolTip(word, content_type = BASIC):
  # toolTip = 'integer: -532; text: "ABCDE"'
  # integer - without "+"
  # text without sign at all
  integer = word2str(word, INT, content_type).lstrip("+")
  text = word2str(word, STR, content_type).lstrip("+-")
  if text.find('?') != -1:
    return  'integer: %s' % integer
  else:
    return  'integer: %s; text: "%s"' % (integer, text)

def word2str(word, type = WORD, content_type = BASIC):
  if content_type != REGJ:
    line = "+" if word[0] == 1 else "-"
  else:
    line = "" # rJ hasn't sign
  if type == WORD:
    for byte in xrange(1 if content_type == BASIC else 4, 6):
      line += " %02i" % word[byte]
    if content_type == REGJ:
      line = line[1:] # remove first space

  elif type == INT:
    line += str(word[1 if content_type == BASIC else 4:5])

  elif type == STR:
    for byte in xrange(1 if content_type == BASIC else 4, 6):
      try:
        line += Device._chr(word[byte])
      except:
        line += "?"
  return line

def str2word(line, type, content_type, allow_mesgBox = False):
  line = line.upper()
  word = Word()
  if len(line) == 0:
    return word
  if line[0] in "+-":
    word[0] = 1 if line[0] == '+' else -1
    line = line[1:]
  else:
    word[0] = 1
  # now line - unsigned part of string

  if type == WORD:
    # take number from the end of line and put tham to the edn of word,
    # if there are not enough nums - zeros putted
    nums = line.split()
    nums = [0] * (5 - len(nums)) + nums # set len(nums) to 5
    len_nums = len(nums)
    for byte in xrange(5, 0, -1):
      word[byte] = min(63, int(nums[byte - 1]))

  elif type == INT:
    i = int(line)
    if content_type == BASIC and i >= 1073741824: # = 64 ** 5
      i = 1073741824 - 1
    elif content_type != BASIC and i >= 4096: # = 64 ** 2
      i = 4096 - 1
    word[1 if content_type == BASIC else 4 :5] = i

  elif type == STR:
    # if len(line) < 5
    if content_type == BASIC:
      # 1) spaces added to the end if it's basic mem cell
      line = line + " " * (5 - len(line)) # set len(line) to 5
    else:
      # 2) rI or rJ: 3 spaces added to the start and some spaces added to the end
      line = "   " + line + " " * (2 - len(line)) # set len(line) to 5
    for byte in xrange(1, 6):
      assert( line[byte - 1] != '?')
      word[byte] = Device._ord(line[byte - 1])
  return word

class WordEdit(QDialog, Ui_Dialog):
  def __init__(self, word, type = BASIC, parent = None):
    QDialog.__init__(self, parent)

    self.setupUi(self)

    self.setWindowTitle(self.tr("Word editing")) # Title: "Word editing"

    self.connect(self.type_word, SIGNAL("toggled(bool)"), self.slot_type_word_changed)
    self.connect(self.type_int, SIGNAL("toggled(bool)"), self.slot_type_int_changed)
    self.connect(self.type_str, SIGNAL("toggled(bool)"), self.slot_type_str_changed)

    self.connect(self, SIGNAL("finished(int)"), self.slot_finished)

    rxsAll = (
      ( # BASIC
        QRegExp("^([+-] )?[0-6]?[0-9]( [0-6]?[0-9]){0,4}$"),
        QRegExp("^[+-]?[0-9]+$"),
        QRegExp("^[+-]?[ A-Za-z0-9~[#.,()+-*/=$<>@;:'?]{0,5}$") # ? - for invalid chars
      ),
      ( # INDEX
        QRegExp("^([+-] )?[0-6]?[0-9]( [0-6]?[0-9]){0,1}$"),
        QRegExp("^[+-]?[0-9]+$"),
        QRegExp("^[+-]?[ A-Za-z0-9~[#.,()+-*/=$<>@;:'?]{0,2}$") # ? - for invalid chars
      ),
      ( # REGJ
        QRegExp("^[0-6]?[0-9]( [0-6]?[0-9]){0,1}$"),
        QRegExp("^[0-9]+$"),
        QRegExp("^[ A-Za-z0-9~[#.,()+-*/=$<>@;:'?]{0,2}$") # ? - for invalid chars
      )
    )

    toolTipsAll = (
      (
        "+ xx xx xx xx xx",
        "+dddddddddd",
        "+ccccc"
      ),
      (
        "+ xx xx",
        "+dddd",
        "+cc"
      ),
      (
        "xx xx",
        "dddd",
        "cc"
      )
    )

    self.content_type = type # basic mem cell, index register or rJ

    self.toolTips = toolTipsAll[self.content_type][:]
    self.rxs = rxsAll[self.content_type][:]

    self.type_word.setToolTip(self.toolTips[WORD])
    self.type_int.setToolTip(self.toolTips[INT])
    self.type_str.setToolTip(self.toolTips[STR])

    self.word = Word(word) # main dialog data
    self.type_changed(WORD, True) # init dialog for WORD type

  def slot_type_word_changed(self, checked):
    self.type_changed(WORD, checked)

  def slot_type_int_changed(self, checked):
    self.type_changed(INT, checked)

  def slot_type_str_changed(self, checked):
    self.type_changed(STR, checked)

  def slot_finished(self, result):
    self.save_value()

  def type_changed(self, type_, checked):
    if checked:
      self.type = type_

      self.input_line.setToolTip(self.toolTips[self.type])
      self.load_value()
    else:
      self.save_value()

  def save_value(self):
    line = str(self.input_line.text()).rstrip()
    if not self.rxs[self.type].exactMatch(line):
      type_str = ("mix word", "integer", "text")[self.type]
      format_str = self.toolTips[self.type]
      msg = self.tr("Input had invalid format.\n\nValid format for %1 is '%2'.").arg(type_str, format_str)
      return QMessageBox.critical(self, self.tr("Input error"), msg)

    if self.type == STR and line.find('?') != -1:
      # we have typied in STR field '?'..
      # it's bad, self.word shouldn't be changed!
      QMessageBox.information(self, self.tr("Information"), self.tr("Text consists '?', so mix word not changed"))
    else:
      if self.type == INT:
        # check if integer is too big ( 1073741824 = 64 ** 5, 4096 = 64 ** 2)
        if  (self.content_type == BASIC and int(line) >= 1073741824) or\
            (self.content_type != BASIC and int(line) >= 4096):
          QMessageBox.information(self, self.tr("Information"), self.tr("Integer was reduced because it was too big"))
      self.word = str2word(line, self.type, self.content_type, allow_mesgBox = True)

  def load_value(self):
    self.input_line.setText(word2str(self.word, self.type, self.content_type))


if __name__ == "__main__":
  app = QApplication(sys.argv)

  mw = WordEdit([-1, 5, 4, 3, 2, 1])
  print mw.exec_(), mw.word

  sys.exit()