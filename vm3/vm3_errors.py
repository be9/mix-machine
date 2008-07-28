class VM3Error(Exception):
  pass

class InvalidAddress(VM3Error):
  pass

class InvalidIndex(VM3Error):
  pass

class InvalidFieldSpec(VM3Error):
  pass

class UnknownInstruction(VM3Error):
  pass

class InvalidCA(VM3Error):
  pass

class NegativeShift(VM3Error):
  pass
