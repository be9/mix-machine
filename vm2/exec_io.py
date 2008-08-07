# in, out, ioc (c_code = 35..37)

# ALL DONE

from word_parser import *
from vm2_errors import *

def _get_device(vmachine):
  """Return device or raise exception"""
  try:
    return vmachine.devices[WordParser.get_field(vmachine)]
  except KeyError:
    raise InvalidDeviceError(WordParser.get_field(vmachine))

def ioc(vmachine):
  vmachine.cycles += 1
  
  dev = _get_device(vmachine)
  
  if dev.busy:
    vmachine.jump_to = vmachine.cur_addr
  else:
    dev.control()

def _in_out(vmachine):
  """Common stuff for IN and OUT"""
  vmachine.cycles += 1
  dev = _get_device(vmachine)
  addr = WordParser.get_full_addr(vmachine, check_mix_addr = True)
  words_num = dev.block_size/5
  if not vmachine.check_mem_addr(addr + words_num - 1):
    raise IOMemRangeError( (words_num, addr, addr + words_num - 1) )
  return (dev, addr, words_num)

def in_(vmachine):
  dev, addr, words_num = _in_out(vmachine)

  if dev.busy:
    vmachine.jump_to = vmachine.cur_addr
    return

  # check if region is writeable
  if not vmachine.is_writeable_set(set(  range(addr, addr + words_num)  )):
    raise MemWriteLockedError( (addr, addr + words_num - 1) )

  # read bytes
  bytes = dev.read((addr, addr + words_num - 1))
  # write them to memory
  for i in xrange(words_num):
    vmachine[addr + i].word_list[1:6] = bytes[5*i: 5*(i + 1)]
  # and lock memory for any actions
  vmachine.locked_cells[vmachine.RW_LOCKED] |= set(range( addr, addr + words_num ))

def out(vmachine):
  dev, addr, words_num = _in_out(vmachine)

  if dev.busy:
    vmachine.jump_to = vmachine.cur_addr
    return

  # check if region is readable
  if not vmachine.is_readable_set(set(  range(addr, addr + words_num)  )):
    raise MemReadLockedError( (addr, addr + words_num - 1) )

  # get bytes list from memory
  bytes = []
  for i in xrange(words_num):
    bytes += vmachine[addr + i].word_list[1:6]
  # write them to file
  dev.write(bytes, (addr, addr + words_num - 1))
  # and lock memory for writing (any instructions can read this memory)
  vmachine.locked_cells[vmachine.W_LOCKED] |= set(range( addr, addr + words_num ))
