import unittest
import sys
import os
import basetestcase

test_modules = {}
for name in ('math', 'load', 'store'): # ADD NEW TESTS HERE
  test_modules[name] = __import__("test_" + name)


def suite(args):
  if len(args) == 0:
    print ">> Testing: all"
    suites = [module.suite for module in test_modules.values()]
  else:
    names = [name for name in test_modules.keys() if name in args]
    print ">> Testing:", " ".join(names)
    suites = [test_modules[name].suite for name in names]

  return unittest.TestSuite(suites)


if __name__ == "__main__":
  from optparse import OptionParser

  parser = OptionParser()
  parser.add_option("-p", "--profile", dest="profile", help="Enable profiling", default=False,
      action="store_true")
  parser.add_option("-v", "--vm N", dest="vm", help="Select VM to use (1 or 2)",
      default="2")

  (options, args) = parser.parse_args()

  if options.vm == "1":
    print ">> Using VM 1"
  else:
    print ">> Using VM 2"
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'vm2'))
    import vm2_vm3
    basetestcase.VM3BaseTestCase.set_vm_class(vm2_vm3.VM3)

  if options.profile:
    print ">> Profiling enabled"

    import hotshot
    import hotshot.stats

    prof = hotshot.Profile("vm.prof")
    exp = prof.runcall(unittest.TextTestRunner().run, suite(args))
    prof.close()
    
    print ">> Please wait for the profiling results..."

    stats = hotshot.stats.load("vm.prof")
    stats.strip_dirs()
    stats.sort_stats('time', 'calls')
    stats.print_stats(40)
  else:
    unittest.TextTestRunner().run(suite(args))
