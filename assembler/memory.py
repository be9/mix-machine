class Memory:
  def __init__(self):
    positive_zero = [+1] + [0] * 5
    self.memory = [ positive_zero[:] for _ in xrange(4000)]

  def cmp_memory(self, memory_dict):
    """Need for testing"""
    positive_zero = [+1] + [0] * 5
    for i in xrange(4000):
      if (i in memory_dict and self.memory[i] != memory_dict[i]) or\
         (i not in memory_dict and self.memory[i] != positive_zero):
        return False

    return True

  def set_byte(self, word_index, byte_index, value):
    """Get valid indexes!"""
    self.memory[word_index][byte_index] = value

  def set_instruction(self, word_index, a_code, i_code, f_code, c_code):
    self.set_byte(word_index, 0, self.sign(a_code))
    self.set_byte(word_index, 1, (self.sign(a_code) * a_code) / 64)
    self.set_byte(word_index, 2, (self.sign(a_code) * a_code) % 64)
    self.set_byte(word_index, 3, i_code)
    self.set_byte(word_index, 4, f_code)
    self.set_byte(word_index, 5, c_code)

  def set_word(self, word_index, value):
    word = self.dec2mix(value)
    for i in xrange(6):
      self.set_byte(word_index, i, word[i])

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
    for i in xrange(r, l - 1, -1): # [r, ..., l]
      word[i] = value_word[5 - r + i]
    if l == 0:
      word[0] = value_word[0]
    return Memory.mix2dec(word)
