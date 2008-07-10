# main_loop.py

# main cycle of assembler

from symbol_table import *

def main_loop(lines):
  # first we need to create table of labels
  labels, local_labels, errors = create_label_table(lines)