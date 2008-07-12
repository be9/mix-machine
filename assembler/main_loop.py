# main_loop.py

# main cycle of assembler

from symbol_table import *
from operations import *

def mix2dec(word):
  return word[0] * (word[5] + (word[4] << 6) + (word[3] << 12) + (word[2] << 18) + (word[1] << 24))

def dec2mix(num):
  mask = (1 << 6) - 1
  u_num = num * sign(num)
  return [sign(num), (u_num & (mask << 24)) >> 24, (u_num & (mask << 18)) >> 18, (u_num & (mask << 12)) >> 12, (u_num & (mask << 6)) >> 6, u_num & mask]

class Memory():
  def __init__(self):
    self.memory = [ ([+1] + [0] * 5)  for _ in xrange(4000)]

  def set_byte(self, word_index, byte_index, value):
    """Get valid indexes!"""
    self.memory[word_index][byte_index] = value

  def set_instruction(self, word_index, a_code, i_code, f_code, c_code):
    self.set_byte(word_index, 0, sign(a_code))
    self.set_byte(word_index, 1, (sign(a_code) * a_code) / 64)
    self.set_byte(word_index, 2, (sign(a_code) * a_code) % 64)
    self.set_byte(word_index, 3, i_code)
    self.set_byte(word_index, 4, f_code)
    self.set_byte(word_index, 5, c_code)

  def set_value(self, word_index, value):
    word = dec2mix(value)
    for i in xrange(6):
      self.set_byte(word_index, i, word[i])

def sign(x):
  if x >= 0:
    return +1
  else:
    return -1


def main_loop(lines, symbol_table):
  """Now we need to assemble program"""
  def check_address(address):
      if not (0 <= address < 4000):
        self.errors.append( (line.line_number, LineNumberError(address)) )

  errors = []
  memory = Memory()
  ca = 0 # current address (*)
  for line in lines:
    # all by 10th and 11th rules from Donald Knuth's book
    if is_instruction(line.operation):
      c_code, f_code_default = get_codes(line.operation)

      # (in the future) a_code, i_code, f_code = parse_argument(line, symbol_table)
      a_part = parse_argument(line, symbol_table)
      i_code = 0
      f_code = f_code_default

      memory.set_instruction(ca, a_part, i_code, f_code, c_code)

      ca += 1
    elif line.operation == "EQU":
      pass
    elif line.operation == "ORIG":
      ca = parse_argument(line, symbol_table)
    elif line.operation == "CON":
      try:
        memory.set_value(ca, parse_argument(line, symbol_table))
      except AssemblySyntaxError, err:
        errors.append( (line.line_number, err) )
      else:
        ca += 1
    elif line.operation == "ALF":
      # FIX ME
      memory.set_value(ca, 20210054) # 20210054 = "ALFFF" = (+1, 1, 13, 6, 6, 6,)
      ca += 1
    elif line.operation == "END":
      # FIX ME: here we put all CON's which comes from smth like "=3="
      try:
        start_address = parse_argument(line, symbol_table)
      except AssemblySyntaxError, err:
        start_address = None
        errors.append( (line.line_number, err) )
      return (memory, start_address, errors) # assemblying finished
