# symbol_table.py

# module for find labels and creating table of them

from operations import *
from errors import *
from parse_argument import *

def is_local_label(label):
  return len(label) == 2 and label[0].isdigit() and label[1] == 'H'

def create_symbol_table(lines):
  labels = {} # {"LABEL" : address, ...}
  local_labels = {} # {"dH" : [(address1, line1), (address2, line2), ...], ...}
  errors = []

  def set_label(line, address): # useful function
    if line.label is not None:
      if line.label in labels:
        errors.append( (line.line_number, RepeatedLabelError(line.label)) )
      elif is_local_label(line.label):
        if line.label in local_labels:
          local_labels[line.label].append( (address, line.line_number) )
        else:
          local_labels[line.label] = [(address, line.line_number)]
      else:
        labels[line.label] = address

  def check_address(address):
     if not (0 <= address < 4000):
       errors.append( (line.line_number, LineNumberError(address)) )

  ca = 0 # current address (*)
  for line in lines:
    # all by 10th and 11th rules from Donald Knuth's book
    if is_instruction(line.operation):
      check_address(ca)
      set_label(line, ca)
      ca += 1
    elif line.operation == "EQU":
      address = parse_argument(line.argument)
      check_address(address)
      set_label(line, address)
    elif line.operation == "ORIG":
      # have bug in Knuth's book. There TABLE must be current address, but there ca+100
      # it's follow from rules and tested in mdk
      check_address(ca)
      set_label(line, ca)
      ca = parse_argument(line.argument)
      check_address(ca)
    elif line.operation in ("CON", "ALF"): # can be combined with first case
      check_address(ca)
      set_label(line, ca)
      ca += 1
    elif line.operation == "END":
      # FIX ME: here we put all CON's which comes from smth like "=3="
      set_label(line, ca)
      break # assemblying finished

  for label in local_labels:
    local_labels[label].sort(None, lambda x: x[1]) # sort by lines

  return (labels, local_labels, errors)
