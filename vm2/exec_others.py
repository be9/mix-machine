# nop (c_code = 0), hlt (c_code = 5, f_code = 2)

# ALL DONE

def nop(vmachine):
  vmachine.cur_addr += 1

def hlt(vmachine):
  vmachine.halted = True
  vmachine.cur_addr += 1
