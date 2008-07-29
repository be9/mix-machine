import unittest
from basetestcase import *

class VM3AddrManipTestCase(VM3BaseTestCase):
  def testENTandENN(self):
    pass

  def testINCandDEC(self):
    pass

suite = unittest.makeSuite(VM3AddrManipTestCase, 'test')

if __name__ == "__main__":
  unittest.TextTestRunner().run(suite)