# in, out, ioc (c_code = 35..37)

# ALL DONE

from word_parser import *
from errors import *

def _get_device(vmachine):
  num = WordParser.get_field(vmachine)
  if num in vmachine.devices:
    return vmachine[num]
  else:
    raise InvalidDeviceError(num)

def ioc(vmachine):
  _get_device(vmachine).control()

def _in(vmachine):
  _get_device(vmachine).read(WordParser.get_full_addr(vmachine, False, True))

def out(vmachine):
  _get_device(vmachine).write(WordParser.get_full_addr(vmachine, False, True))
