
class Device:
  def __init__(self, vmachine, mode, block_size, block_time):
    self.vmachine = vmachine
    self.mode = mode # [rw]
    self.block_size = block_size # number of words for blocking
    self.block_time = block_time # time for blocking
    self.busy = False
    self.busy_time = 0 # how many cycles device has been busy

  def read(self, addr):
    if 'r' not in self.mode:
      raise UnsupportedDeviceModeError("inputing")
    pass

  def write(self, addr):
    if 'w' not in self.mode:
      raise UnsupportedDeviceModeError("outputing")
    pass

  def control(self):
    pass
