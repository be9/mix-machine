# inc, dec, ent, enn

def _ent(vmachine, addr, reg): # getr - function to GET Register from
  vmachine.__dict__[reg] = vmachine.dec2mix(addr)

def enta(vmachine, addr):
  _ent(vmachine, addr, "rA")
  vmachine.cur_addr += 1

def entx(vmachine, addr):
  _ent(vmachine, addr, "rX")
  vmachine.cur_addr += 1