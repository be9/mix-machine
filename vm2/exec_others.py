# nop, hlt

def nop(vmachine):
  vmachine.cur_addr += 1

def hlt(vmachine):
  vmachine.halted = True
  vmachine.cur_addr += 1