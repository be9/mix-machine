__all__ = [ 'Memory' ]

MEMORY_SIZE = 4000

class Memory:
  @staticmethod
  def positive_zero():
    return [1, 0 ,0 ,0 ,0 ,0]

  def __init__(self):
    self.memory = [ self.positive_zero()[:] for _ in xrange(MEMORY_SIZE)]

  def __getitem__(self, index):
    return self.memory[index]

  def __setitem__(self, index, value):
    word = self.dec2mix(value)

    if self.is_valid_address(index):
      self.memory[index][:] = word[:]

  def set_sign(self, index, sign):
    if self.is_valid_address(index):
      self.memory[index][0] = sign

  def __cmp__(self, memory_dict):
    """Need for testing"""
    
    positive_zero = self.positive_zero()
    
    if not isinstance(memory_dict, dict) or \
       any( (i     in memory_dict and self[i] != memory_dict[i]) or
            (i not in memory_dict and self[i] != positive_zero)
            for i in xrange(MEMORY_SIZE)):
      return 1
    else:
      return 0
  
  def is_valid_address(self, adr):
    return 0 <= adr < len(self.memory)
    
  @staticmethod
  def mix2dec(word):
    return word[0] * reduce(lambda x,y: (x << 6) | y, word[1:], 0)

  @staticmethod
  def dec2mix(num):
    mask = 63     # 1<<6 - 1
    u_num = abs(num)

    return [Memory.sign(num)] + [ (u_num >> shift) & mask for shift in xrange(24, -1, -6) ]

  @staticmethod
  def sign(x):
    if x >= 0:
      return +1
    else:
      return -1

  @staticmethod
  def apply_to_word(value, word, field):
    l = field / 8
    r = field % 8
    if not ( 0 <= l <= 5 and 0 <= r <= 5 and l <= r ):
      return None
    value_word = Memory.dec2mix(value)
    for i in xrange(r, max(l - 1, 0), -1): # [r, ..., l]
      word[i] = value_word[5 - r + i]
    if l == 0:
      word[0] = value_word[0]
    return Memory.mix2dec(word)
