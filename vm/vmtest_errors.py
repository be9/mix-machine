class VMTestingError(Exception):
  pass

class InvalidAddress(VMTestingError):
  pass

class InvalidIndex(VMTestingError):
  pass

class InvalidFieldSpec(VMTestingError):
  pass

class UnknownInstruction(VMTestingError):
  pass

class InvalidCA(VMTestingError):
  pass

class NegativeShift(VMTestingError):
  pass

class InvalidMove(VMTestingError):
  pass

class InvalidDevice(VMTestingError):
  pass

class UnsupportedDeviceMode(VMTestingError):
  pass

class InvalidChar(VMTestingError):
  pass

class InvalidCharCode(VMTestingError):
  pass

class IOMemRange(VMTestingError):
  pass

class ReadLocked(VMTestingError):
  pass

class WriteLocked(VMTestingError):
  pass