# nop, hlt

def nop(vmachine, addr, ind, f, c):
  vmachine.cur_addr += 1

def hlt(vmachine, addr, ind, f, c):
  vmachine.halted = True
  vmachine.cur_addr += 1