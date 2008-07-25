# inc, dec, ent, enn

def _ent(vmachine, reg): # getr - function to GET Register from
  vmachine.__dict__[reg] = vmachine.dec2mix(vmachine.word_parser.get_full_addr())

def enta(vmachine):
  _ent(vmachine, "rA")
  vmachine.cur_addr += 1

def entx(vmachine):
  _ent(vmachine, "rX")
  vmachine.cur_addr += 1