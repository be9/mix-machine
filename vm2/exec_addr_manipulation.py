# inc, dec, ent, enn

#------------------ENT------------------
def _ent(vmachine, reg): # getr - function to GET Register from
  vmachine.__dict__["r" + reg] = vmachine.dec2mix(vmachine.word_parser.get_full_addr())
  vmachine.cur_addr += 1

def enta(vmachine):
  _ent(vmachine, "A")

def entx(vmachine):
  _ent(vmachine, "X")


#------------------INC------------------
def _inc(vmachine, reg):
  vmachine.__dict__["r" + reg] = vmachine.sum_words(
                                    vmachine.__dict__["r" + reg],
                                    vmachine.dec2mix(vmachine.word_parser.get_full_addr())
                                 )
  vmachine.clear_rI(reg)
  vmachine.cur_addr += 1

def inc1(vmachine):
  _inc(vmachine, "1")

def inc2(vmachine):
  _inc(vmachine, "2")

def inc3(vmachine):
  _inc(vmachine, "2")

def inc4(vmachine):
  _inc(vmachine, "2")

def inc5(vmachine):
  _inc(vmachine, "2")

def inc6(vmachine):
  _inc(vmachine, "2")