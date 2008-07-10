# main_cycle.py

# main cycle of assembler

from label_table import *

def main_cycle(lines):
  # first we need to create table of labels
  labels, errors = create_label_table(lines)
  print labels, errors
  for error in errors:
    print error[1]