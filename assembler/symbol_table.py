# symbol_table.py

# module for find labels and creating table of them

from parse_argument import *
from operations import *
from errors import *

def is_local_label(label):
  return len(label) == 2 and label[0].isdigit() and label[1] in ('H', 'h')

def is_local_label_reference(label):
  return len(label) == 2 and label[0].isdigit() and label[1] in ('F', 'B', 'f', 'b')

def is_label(s):
  return s.isalnum() and any(ch.isalpha() for ch in s) and \
    not is_local_label_reference(s)
  
class SymbolTable:
  def __init__(self, lines, labels = None, local_labels = None, literals = None, end_address = None):
    if labels is not None:
      self.labels = labels # {"LABEL" : address, ...}
    else:
      self.labels = {}
    if local_labels is not None:
      self.local_labels = local_labels
    else:
      self.local_labels = {} # {"dH" : [(address1, line1), (address2, line2), ...], ...}
    if literals is not None:
      self.literals = literals
    else:
      self.literals = [] # [value1, value2, ...]
    self.errors = []
    self.end_address = end_address # None means that it is not set yet
    self.literal_number = 0 # None means that it is not set yet
    
    if lines is None: # need for testing
      return

    def set_label(line, address): 
      """Useful function"""
      if line.label is not None:
        if line.label in self.labels:
          self.errors.append( (line.line_number, RepeatedLabelError(line.label)) )
        elif is_local_label(line.label):
          if line.label in self.local_labels:
            self.local_labels[line.label].append( (address, line.line_number) )
          else:
            self.local_labels[line.label] = [(address, line.line_number)]
        else:
          self.labels[line.label] = address

    def check_address(address):
      if not (0 <= address < 4000):
        self.errors.append( (line.line_number, LineNumberError(address)) )

    def set_literal(value):
      self.literals.append(value) # it's queue. first added values would be first popped
                                  # in assembler to put them in the end or program

    ca = 0 # current address (*) 
    for line in lines:
      # all by 10th and 11th rules from Donald Knuth's book
      if is_instruction(line.operation):
        check_address(ca)
        set_label(line, ca)
        try:
          res = parse_argument(line, self, ca)
        except AssemblySyntaxError:
          pass # it will be excepted in assembler :)
        except HaveLiteralException, e:
          set_literal(e.value)
        ca += 1
      elif line.operation == "EQU":
        try:
          address = parse_argument(line, self, ca)
          set_label(line, address)
        except AssemblySyntaxError, err:
          self.errors.append( (line.line_number, err) )
      elif line.operation == "ORIG":
        # have bug in Knuth's book. There TABLE must be current address, but there ca+100
        # it's follow from rules and tested in mdk
        check_address(ca)
        set_label(line, ca)
        try:
          ca = parse_argument(line, self, ca)
        except AssemblySyntaxError, err:
          self.errors.append( (line.line_number, err) )
        check_address(ca)
      elif line.operation in ("CON", "ALF"): # can be combined with first case
        check_address(ca)
        set_label(line, ca)
        ca += 1
      elif line.operation == "END":
        self.end_address = ca
        set_label(line, ca)
        break # assemblying finished

    for label in self.local_labels:
      self.local_labels[label].sort(None, lambda x: x[1]) # sort by line numbers

  def find(self, label, line_number):
    """Returns address or None"""
    if label in self.labels:
      return self.labels[label]

    # find in local_labels
    if is_local_label_reference(label):
      local_label = label[0] + 'H'
      if local_label in self.local_labels:

        b_label, f_label = None, None
        for x in self.local_labels[local_label]:
          if x[1] < line_number:
            b_label = x
          if x[1] > line_number:
            f_label = x
            break

        if label[1] == 'B' and b_label is not None:
          return b_label[0]
        elif label[1] == 'F' and f_label is not None:
          return f_label[0]

      raise InvalidLocalLabelError(label)

    return None
