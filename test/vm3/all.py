import unittest
import sys
import os
import basetestcase

test_modules = {}
module_names = ('load', 'store', 'math', 'addr_manip', 'cmp') # ADD NEW TESTS HERE
for name in module_names:
  test_modules[name] = __import__("test_" + name)


def suite(args):
  if len(args) == 0:
    names = module_names
  else:
    names = [name for name in module_names if name in args]
  print ">> Testing:", " ".join(names)
  suites = [test_modules[name].suite for name in names]

  return unittest.TestSuite(suites)


if __name__ == "__main__":
  from optparse import OptionParser

  parser = OptionParser()
  parser.add_option("-p", "--profile", dest="profile", help="enable profiling", default=False,
      action="store_true")
  parser.add_option("-v", "--vm N", dest="vm", help="select VM to use (1 or 2)",
      default="2")
  parser.set_usage("all.py [OPTIONS] [NAMES]")

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
