# inc, dec, ent, enn
from word_parser import *

#------------------ENT------------------
def _ent(vmachine, reg): # getr - function to GET Register from
  vmachine.__dict__["r" + reg] = Word(WordParser.get_full_addr(vmachine))
  vmachine.cur_addr += 1

def enta(vmachine):
  _ent(vmachine, "A")

def entx(vmachine):
  _ent(vmachine, "X")


#------------------INC------------------
def _inc(vmachine, reg):
  vmachine.__dict__["r" + reg] = Word( vmachine.__dict__["r" + reg][:] + WordParser.get_full_addr(vmachine) )
  if vmachine.clear_rI(reg):
    #FIX ME - overflow
    pass
  vmachine.cur_addr += 1

def inc1(vmachine):
  _inc(vmachine, "1")

def inc2(vmachine):
  _inc(vmachine, "2")

def inc3(vmachine):
  _inc(vmachine, "3")

def inc4(vmachine):
  _inc(vmachine, "4")

def inc5(vmachine):
  _inc(vmachine, "5")

def inc6(vmachine):
  _inc(vmachine, "6")