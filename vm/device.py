from vm_errors import *

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import charset

class DeviceBusyException(Exception):
  pass

class Device:
  """Abstract class of device"""
  def __init__(self, mode, block_size, lock_time):
    self.mode = mode # [rw]
    self.block_size = block_size # number of bytes in one block
    self.lock_time = lock_time # time for blocking device
    self.busy = False
    self.time_left = 0 # how many cycles device will be busy more

    # next 2 variables for memory locking
    self.locked_mode = None # "w" or "rw"
    self.locked_range = (None, None) # left, right limits

  @staticmethod
  def _ord(char):
    """Char -> Int"""
    res = charset.ord(char)
    if res is not None:
      return res
    else:
      raise InvalidCharError(char)
  @staticmethod
  def _chr(num):
    """Int -> Char"""
    res = charset.chr(num)
    if res is not None:
      return res
    else:
      raise InvaliCharCodeError(num)

  def read(self, limits):
    """Basics of reading for any device"""
    if 'r' not in self.mode:
      raise UnsupportedDeviceModeError("inputting")
    if self.busy:
      raise DeviceBusyException
    
    self.busy = True
    self.time_left = self.lock_time # add time for new read

    self.locked_mode = "rw"
    self.locked_range = limits

  def write(self, bytes, limits):
    """Basics of writing for any device"""
    assert(len(bytes) == self.block_size)
    if 'w' not in self.mode:
      raise UnsupportedDeviceModeError("outputting")
    if self.busy:
      raise DeviceBusyException
   
    self.busy = True
    self.time_left = self.lock_time # add time for new write

    self.locked_mode = "w"
    self.locked_range = limits

  def control(self):
    """Control function, called by IOC instruction"""
    if self.busy:
      raise DeviceBusyException
    
    self.busy = True
    self.time_left = self.lock_time # add time for control

    self.locked_mode = ""
    self.locked_range = None

  def refresh(self, cycles_passed):
    """Called every VM step, if device is busy, refresh how many cycles it'll busy more"""
    if not self.busy:
      return None
    self.time_left -= cycles_passed
    if self.time_left <= 0:
      self.busy = False
      self.time_left = 0
      return (self.locked_mode, self.locked_range)
    return None


class FileDevice(Device):
  """Device that can read(write) from(to) files"""
  def __init__(self, mode, block_size, lock_time, file_object):
    assert( ('r' in mode) ^ ('w' in mode) )
    Device.__init__(self, mode, block_size, lock_time)
    self.file_object = file_object

  def read(self, limits):
    """Read from file minimum from one line or <block_size> chars"""
    Device.read(self, limits)

    line = self.file_object.readline().rstrip("\n\r")
    if len(line) < self.block_size:
      line += " " * (self.block_size - len(line))
    else:
      line = line[:self.block_size]
    bytes = map(Device._ord, line)
    return bytes

  def write(self, bytes, limits):
    """Write <block_size> chars to file"""
    Device.write(self, bytes, limits)

    line = "".join(map(Device._chr, bytes))
    self.file_object.write(line+"\n")

  def control(self):
    """Jump to newline in file"""
    Device.control(self)

    if 'r' in self.mode:
      self.file_object.readline() # simply jump newline
    else: # 'w' in self.mode:
      self.file_object.write("<---------NEW-PAGE--------->\n") # jump newline
