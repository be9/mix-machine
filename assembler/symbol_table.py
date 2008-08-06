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
  def __init__(self, labels = None, local_labels = None, literals = None):
    self.literals = []     if literals     is None else literals
    self.labels = {}       if labels       is None else labels
    self.local_labels = {} if local_labels is None else local_labels

  def set_label(self, label, address, lineno): 
    if label is None:
      return

    if is_local_label(label):
      self.local_labels.setdefault(label, []).append( (address, lineno) )
    else:
      if label in self.labels:
        raise RepeatedLabelError(label)
      
      self.labels[label] = address

  def add_literal(self, value_and_sign):
    """This is called on the 2nd pass from parse_argument. Returns an address for the value"""
    self.literals.append(value_and_sign) 
    self.literal_address += 1
    return self.literal_address - 1

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
