
class Device:
  def __init__(self, vmachine, mode, block_size):
    self.vmachine = vmachine
    self.mode = mode # [rw]
    self.busy = False
    self.block_size = block_size

  def read(self):
    if 'r' not in self.mode:
      return # raise error
    pass

  def write(self):
    if 'w' not in self.mode:
      return # raise error
    pass
