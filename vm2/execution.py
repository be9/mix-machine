
from vm2_errors import *

import exec_all

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from disasm import Disasm

def execute(vmachine):
  # some common stuff
  if not vmachine.is_readable(vmachine.cur_addr):
    raise MemReadLockedError( (vmachine.cur_addr, vmachine.cur_addr) )

  proc_name = Disasm.disasm(vmachine.get_cur_word())[0]

  if proc_name is not None:
    vmachine.jump_to = None
    before_cycles = vmachine["cycles"]

    exec_all.__dict__[proc_name](vmachine)

    if vmachine.jump_to is None:
      vmachine["cur_addr"] += 1
    else:
      vmachine["cur_addr"] = vmachine.jump_to

    return vmachine["cycles"] - before_cycles
  else:
    raise UnknownInstructionError(tuple(word))
