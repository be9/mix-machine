# inc, dec, ent, enn

def _ent(vmachine, addr, ind, f, c, r): # getr - function to GET Register from
  vmachine.__dict__[r] = vmachine.dec2mix(addr)

def enta(vmachine, addr, ind, f, c):
  _ent(vmachine, addr, ind, f, c, "rA")
  vmachine.cur_addr += 1

def entx(vmachine, addr, ind, f, c):
  _ent(vmachine, addr, ind, f, c, "rX")
  vmachine.cur_addr += 1