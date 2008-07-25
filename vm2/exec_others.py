# nop, hlt

def nop(vmachine, addr):
  vmachine.cur_addr += 1

def hlt(vmachine, addr):
  vmachine.halted = True
  vmachine.cur_addr += 1