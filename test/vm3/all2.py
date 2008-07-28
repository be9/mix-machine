import unittest
import os
import sys
import basetestcase
import all

if __name__ == "__main__":
  sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'vm2'))
  import vm2_vm3
  basetestcase.VM3BaseTestCase.set_vm_class(vm2_vm3.VM3)
  unittest.TextTestRunner().run(all.suite())
