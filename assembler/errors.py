# errors.py

# module of work with errors

# error codes of interface:
ERR_INVALID_ARGS = (1, "Invalid command line arguments, required one existing file name and name for output file (optionally)")
ERR_INVALID_INPUT_FILE = (2, "Can't open input file")
ERR_INVALID_OUTPUT_FILE = (3, "Can't create output file")

# error codes of assembler
ERR_SYNTAX = (1000, "Syntax errors in source file")
ERR_ASSEMBLE = (1001, "Assembler errors in source file")

class AssemblyError(Exception):
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

class MissingOperationError(AssemblyError):
  """Syntax error, operation missing"""

class InvalidLabelError(AssemblyError):
  """Invalid label name (%s)"""

class TooLongLabelError(AssemblyError):
  """Too long label name (%s)"""

class UnknownOperationError(AssemblyError):
  """Unknown operation (%s)"""

class RepeatedLabelError(AssemblyError):
  """This label name used twice (%s)"""

class LineNumberError(AssemblyError):
  """This address (%s) is invalid in MIX computer"""

class NoEndError(AssemblyError):
  """Required operation (END) wasn't found"""

class InvalidLocalLabelError(AssemblyError):
  """Invalid local label (%s) (no dH label found)"""

class ArgumentRequiredError(AssemblyError):
  """Argument required for this operation (%s)"""

class UnquotedStringError(AssemblyError):
  """Unqouted string (%s)"""

class InvalidCharError(AssemblyError):
  """This char is invalid in MIX computer (%s)"""

class ExpectedSExpError(AssemblyError):
  """Expected correct simple expression after '%s'"""

class ExpectedExpError(AssemblyError):
  """Expected correct expression after '%s'"""

class NoClosedBracketError(AssemblyError):
  """Expected closing bracket after '%s'"""

class NoEqualSignError(AssemblyError):
  """Expected equal sign after '%s'"""

class InvalidFieldSpecError(AssemblyError):
  """Invalid field specification (%s)"""

class InvalidIndError(AssemblyError):
  """Invalid index (%s)"""

class InvalidAddrError(AssemblyError):
  """Invalid address (%s)"""

class ExpectedWExpError(AssemblyError):
  """Expected correct W-expression (%s)"""

class UnexpectedStrInTheEndError(AssemblyError):
  """Unexpected string in the end of argument (%s)"""

class TooLongLiteralError(AssemblyError):
  """Too long literal expression, must be shorter than 10 digits (%s)"""

class NoFreeSpaceForLiteralsError(AssemblyError):
  """After END there are no memory to store all literals"""

class FieldFixedError(AssemblyError):
  """Field part for this instruction is fixed (%s), can't be changed"""
