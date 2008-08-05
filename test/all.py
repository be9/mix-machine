import unittest
import assembler.all
import vm2.all

def suite():
  return unittest.TestSuite(
    (
  	  assembler.all.suite(),
  	  vm2.all.suite()
    )
  )

unittest.TextTestRunner().run(suite())

