# label_table.py

# module for find labels and creating table of them

from operations import *
from errors import *
from parse_argument import *


def create_label_table(lines):
  labels = {} # {"LABEL" : address, ...}
  errors = []

  def set_label(line, address): # useful function
    if line.label is not None:
      if line.label in labels:
        errors.append( (line.line_number, RepeatedLabelError(line.label)) )
      else:
        labels[line.label] = address

  def check_address(address):
     if not (0 <= address < 4000):
       errors.append( (line.line_number, LineNumberError(address)) )

  ca = 0 # current address (*)
  for line in lines:
    # all by 10th and 11th rules from Donald Knuth's book
    if is_function(line.operation):
      set_label(line, ca)
      ca += 1
    elif line.operation == "EQU":
      address = parse_argument(line.argument)
      check_address(address)
      set_label(line, address)
    elif line.operation == "ORIG":
      # have bug in Knuth's book. There TABLE must be current address, but there ca+100
      # it's follow from rules and tested in mdk
      set_label(line, ca)
      ca = parse_argument(line.argument)
    elif line.operation == "CON" or line.operation == "ALF": # can be combined with first case
      set_label(line, ca)
      ca += 1
    elif line.operation == "END":
      set_label(line, ca)
      break # assemblying finished
    check_address(ca)

  return (labels, errors)
