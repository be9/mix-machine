from vm2_errors import *

# tables are copied from mdk manual (10, 20, 21 = delta, sigma, pi)
ord_table = {
    " ":  0,      "A":  1,      "B":  2,      "C":  3,
    "D":  4,      "E":  5,      "F":  6,      "G":  7,
    "H":  8,      "I":  9,      "~":  10,     "J":  11,
    "K":  12,     "L":  13,     "M":  14,     "N":  15,
    "O":  16,     "P":  17,     "Q":  18,     "R":  19,
    "[":  20,     "#":  21,     "S":  22,     "T":  23,
    "U":  24,     "V":  25,     "W":  26,     "X":  27,
    "Y":  28,     "Z":  29,     "0":  30,     "1":  31,
    "2":  32,     "3":  33,     "4":  34,     "5":  35,
    "6":  36,     "7":  37,     "8":  38,     "9":  39,
    ".":  40,     ",":  41,     "(":  42,     ")":  43,
    "+":  44,     "-":  45,     "*":  46,     "/":  47,
    "=":  48,     "$":  49,     "<":  50,     ">":  51,
    "@":  52,     ";":  53,     ":":  54,     "'":  55
}
chr_table = [x for x in " ABCDEFGHI~JKLMNOPQR[#STUVWXYZ0123456789.,()+-*/=$<>@;:'"]

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
    try:
      return ord_table[char]
    except:
      raise InvalidCharError(char)
  @staticmethod
  def _chr(num):
    """Int -> Char"""
    try:
      return chr_table[num]
    except:
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
  def __init__(self, mode, block_size, busy_time, file_object):
    assert( ('r' in mode) ^ ('w' in mode) )
    Device.__init__(self, mode, block_size, busy_time)
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
