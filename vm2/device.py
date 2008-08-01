from errors import *

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


class Device:
  def __init__(self, mode, block_size, busy_time):
    self.mode = mode # [rw]
    self.block_size = block_size # number of bytes in one block
    self.busy_time = busy_time # time for blocking device
    self.busy = False
    self.time_left = 0 # how many cycles device will be busy more
    self.locked_mode = None # "w" or "rw"
    self.locked_range = (None, None) # left, right limits

  @staticmethod
  def _ord(char):
    try:
      return ord_table[char]
    except:
      raise InvalidCharError(char)
  @staticmethod
  def _chr(num):
    try:
      return chr_table[num]
    except:
      raise InvaliCharCodeError(num)

  def read(self):
    if 'r' not in self.mode:
      raise UnsupportedDeviceModeError("inputing")
    self.busy = True
    self.time_left += self.busy_time # add time for new read

  def write(self, bytes):
    assert(len(bytes) == self.block_size)
    if 'w' not in self.mode:
      raise UnsupportedDeviceModeError("outputing")
    self.busy = True
    self.time_left += self.busy_time # add time for new write

  def control(self):
    self.busy = True
    self.time_left += self.busy_time # add time for control

  def refresh(self, cycles_passed):
    if not self.busy:
      return None
    self.time_left -= cycles_passed
    if self.time_left <= 0:
      self.busy = False
      self.time_left = 0
      return (self.locked_mode, self.locked_range)
    return None


class FileDevice(Device):
  def __init__(self, mode, block_size, busy_time, file_object):
    assert( ('r' in mode) ^ ('w' in mode) )
    Device.__init__(self, mode, block_size, busy_time)
    self.file_object = file_object

  def read(self):
    Device.read(self)

    line = ""
    while len(line) < self.block_size:
      char = self.file_object.read(1)
      if char not in "\r\n":
        line += char
      else:
        self.file_object.readline() # jump newline
        line += " " * (self.block_size - len(line))
        break
    bytes = map(Device._ord, line)
    return bytes

  def write(self, bytes):
    Device.write(self, bytes)

    line = "".join(map(Device._chr, bytes))
    self.file_object.write(line)

  def control(self):
    Device.control(self)

    if 'r' in mode:
      self.file_object.readline() # jump newline
    else: # 'w' in mode:
      self.file_object.write("\n") # jump newline
