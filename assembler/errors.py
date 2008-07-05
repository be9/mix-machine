# errors.py

# module of work with errors

# error codes of interface:
ERR_INVALID_ARGS = [1, "Invalid command line arguments, required one existing file name and name for output file (optionally)"]
ERR_INVALID_INPUT_FILE = [2, "Can't open input file"]
ERR_FILE = [3, "Fatal error with working with files"]

# error codes of assembler
ERR_LONG_LABEL = [1001, "Label name can't consist more than 10 letters or digits"]
ERR_BAD_LABEL = [1002, "Label name consist invalid characters (should be only letters (one required) and digits)"]
