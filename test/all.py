import unittest
import assembler.all
import vm.all

def suite():
  return unittest.TestSuite(
    (
  	  assembler.all.suite(),
  	  vm.all.suite()
    )
  )

unittest.TextTestRunner().run(suite())

