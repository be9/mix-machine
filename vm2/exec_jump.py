# j* (c_code = 34, 38..47)

# done all but JBUS and JRED

from word_parser import *

def _j(vmachine, condition, save_j = True, reset_of = False):
  vmachine.cycles += 1

  if not condition(vmachine):
    return

  if reset_of:
    vmachine.of = False

  if save_j:
    vmachine.rJ[4:5] = vmachine.cur_addr + 1

  vmachine.jump_to = WordParser.get_full_addr(vmachine, False, True)

#def jbus(vmachine): _j(vmachine, lambda vm: True)
#def jred(vmachine): _j(vmachine, lambda vm: True)

def jmp(vmachine):    _j(vmachine, lambda vm: True)
def jsj(vmachine):    _j(vmachine, lambda vm: True, save_j = False)
def jov(vmachine):    _j(vmachine, lambda vm: vm.of == True, reset_of = 1)
def jnov(vmachine):   _j(vmachine, lambda vm: vm.of == False)
def jl(vmachine):     _j(vmachine, lambda vm: vm.cf < 0)
def je(vmachine):     _j(vmachine, lambda vm: vm.cf == 0)
def jg(vmachine):     _j(vmachine, lambda vm: vm.cf > 0)
def jge(vmachine):    _j(vmachine, lambda vm: vm.cf >= 0)
def jne(vmachine):    _j(vmachine, lambda vm: vm.cf != 0)
def jle(vmachine):    _j(vmachine, lambda vm: vm.cf <= 0)

def jan(vmachine):    _j(vmachine, lambda vm: vm.rA[:] < 0)
def jaz(vmachine):    _j(vmachine, lambda vm: vm.rA[:] == 0)
def jap(vmachine):    _j(vmachine, lambda vm: vm.rA[:] > 0)
def jann(vmachine):   _j(vmachine, lambda vm: vm.rA[:] >= 0)
def janz(vmachine):   _j(vmachine, lambda vm: vm.rA[:] != 0)
def janp(vmachine):   _j(vmachine, lambda vm: vm.rA[:] <= 0)

def j1n(vmachine):    _j(vmachine, lambda vm: vm.r1[:] < 0)
def j1z(vmachine):    _j(vmachine, lambda vm: vm.r1[:] == 0)
def j1p(vmachine):    _j(vmachine, lambda vm: vm.r1[:] > 0)
def j1nn(vmachine):   _j(vmachine, lambda vm: vm.r1[:] >= 0)
def j1nz(vmachine):   _j(vmachine, lambda vm: vm.r1[:] != 0)
def j1np(vmachine):   _j(vmachine, lambda vm: vm.r1[:] <= 0)

def j2n(vmachine):    _j(vmachine, lambda vm: vm.r2[:] < 0)
def j2z(vmachine):    _j(vmachine, lambda vm: vm.r2[:] == 0)
def j2p(vmachine):    _j(vmachine, lambda vm: vm.r2[:] > 0)
def j2nn(vmachine):   _j(vmachine, lambda vm: vm.r2[:] >= 0)
def j2nz(vmachine):   _j(vmachine, lambda vm: vm.r2[:] != 0)
def j2np(vmachine):   _j(vmachine, lambda vm: vm.r2[:] <= 0)

def j3n(vmachine):    _j(vmachine, lambda vm: vm.r3[:] < 0)
def j3z(vmachine):    _j(vmachine, lambda vm: vm.r3[:] == 0)
def j3p(vmachine):    _j(vmachine, lambda vm: vm.r3[:] > 0)
def j3nn(vmachine):   _j(vmachine, lambda vm: vm.r3[:] >= 0)
def j3nz(vmachine):   _j(vmachine, lambda vm: vm.r3[:] != 0)
def j3np(vmachine):   _j(vmachine, lambda vm: vm.r3[:] <= 0)

def j4n(vmachine):    _j(vmachine, lambda vm: vm.r4[:] < 0)
def j4z(vmachine):    _j(vmachine, lambda vm: vm.r4[:] == 0)
def j4p(vmachine):    _j(vmachine, lambda vm: vm.r4[:] > 0)
def j4nn(vmachine):   _j(vmachine, lambda vm: vm.r4[:] >= 0)
def j4nz(vmachine):   _j(vmachine, lambda vm: vm.r4[:] != 0)
def j4np(vmachine):   _j(vmachine, lambda vm: vm.r4[:] <= 0)

def j5n(vmachine):    _j(vmachine, lambda vm: vm.r5[:] < 0)
def j5z(vmachine):    _j(vmachine, lambda vm: vm.r5[:] == 0)
def j5p(vmachine):    _j(vmachine, lambda vm: vm.r5[:] > 0)
def j5nn(vmachine):   _j(vmachine, lambda vm: vm.r5[:] >= 0)
def j5nz(vmachine):   _j(vmachine, lambda vm: vm.r5[:] != 0)
def j5np(vmachine):   _j(vmachine, lambda vm: vm.r5[:] <= 0)

def j6n(vmachine):    _j(vmachine, lambda vm: vm.r6[:] < 0)
def j6z(vmachine):    _j(vmachine, lambda vm: vm.r6[:] == 0)
def j6p(vmachine):    _j(vmachine, lambda vm: vm.r6[:] > 0)
def j6nn(vmachine):   _j(vmachine, lambda vm: vm.r6[:] >= 0)
def j6nz(vmachine):   _j(vmachine, lambda vm: vm.r6[:] != 0)
def j6np(vmachine):   _j(vmachine, lambda vm: vm.r6[:] <= 0)

def jxn(vmachine):    _j(vmachine, lambda vm: vm.rX[:] < 0)
def jxz(vmachine):    _j(vmachine, lambda vm: vm.rX[:] == 0)
def jxp(vmachine):    _j(vmachine, lambda vm: vm.rX[:] > 0)
def jxnn(vmachine):   _j(vmachine, lambda vm: vm.rX[:] >= 0)
def jxnz(vmachine):   _j(vmachine, lambda vm: vm.rX[:] != 0)
def jxnp(vmachine):   _j(vmachine, lambda vm: vm.rX[:] <= 0)
