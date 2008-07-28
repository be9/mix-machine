# test_symbol_table.py

# testing of module label_table

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'assembler'))
from parse_line import Line
from symbol_table import *

class LabelsTestCase(unittest.TestCase):
  def test_is_label(self):
    for l in 'blah a z 123y321 1a1 a1 1a 123456789a 9H labellabel 40F 40B F B'.split():
      self.assertEqual(is_label(l), True)

    for l in '4F 4B 0F 0B 9F 9B 123 1 2 label* # % label,'.split():
      self.assertEqual(is_label(l), False)
  
  def test_is_local_label(self):
    for i in xrange(0,10):
      self.assertEqual(is_local_label('%dH' % i), True)
      self.assertEqual(is_local_label('%dh' % i), True)

    for l in '1F 1B blah 10H 123 4Q4'.split():
      self.assertEqual(is_local_label(l), False)

  def test_is_local_label_reference(self):
    for i in xrange(0,10):
      self.assertEqual(is_local_label_reference('%df' % i), True)
      self.assertEqual(is_local_label_reference('%dF' % i), True)
      self.assertEqual(is_local_label_reference('%db' % i), True)
      self.assertEqual(is_local_label_reference('%dB' % i), True)
      self.assertEqual(is_local_label_reference('%dH' % i), False)
      self.assertEqual(is_local_label_reference('%dh' % i), False)
  
suite = unittest.makeSuite(LabelsTestCase, 'test')

if __name__ == "__main__":
	unittest.main()
