# errors.py

# module of work with errors

# error codes of interface:
ERR_INVALID_ARGS = (1, "Invalid command line arguments, required one existing file name and name for output file (optionally)")
ERR_INVALID_INPUT_FILE = (2, "Can't open input file")
ERR_FILE = (3, "Fatal error with working with files")

# error codes of assembler
ERR_SYNTAX = (1000, "Syntax errors in source file")

class AssemblySyntaxError(Exception):
  def __init__(self, info = None):
    self.info = info

  def __str__(self):
    if self.__doc__ is not None:
      try:
        return self.__doc__ % self.info
      except:
        return self.__doc__
    else:
      return str(self.info)

  def __cmp__(self, another):
    return cmp(self.__str__(), another.__str__())

class MissingOperationError(AssemblySyntaxError):
  """Syntax error, operation missing"""

class InvalidLabelError(AssemblySyntaxError):
  """Invalid label name (%s)"""

class TooLongLabelError(AssemblySyntaxError):
  """Too long label name (%s)"""

class UnknownOperationError(AssemblySyntaxError):
  """Unknown operation: %s"""

class RepeatedLabelError(AssemblySyntaxError):
  """This label name used twice (%s)"""

class LineNumberError(AssemblySyntaxError):
  """This address (%s) is invalid in MIX computer"""

