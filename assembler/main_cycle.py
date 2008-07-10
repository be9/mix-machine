# main_cycle.py

# main cycle of assembler

from label_table import *

def main_cycle(lines):
  # first we need to create table of labels
  labels, local_labels, errors = create_label_table(lines)