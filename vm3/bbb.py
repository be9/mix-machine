class YetAnotherVMContext:
  def __init__(self):
    self.regs = dict(A=0, X=0, I1=0, I2=0, I3=0, I4=0, I5=0, I6=0, J=0)
    self.ca = 0
    self.of = False
    self.cf = 0
    self.memory = [0] * 4000

class TestedVirtualMachine:
  def __init__(self):
    self.context = YetAnotherVMContext()

initial_context = {
  'A': [+1, 11, 22, 33, 44, 55],
  'X': [-1, 22, 33, 44, 55, 11].
  'I1': [+1, 0, 0, 0, 10, 20],
  'I2': [-1, 0, 0, 0, 22, 33],
  'I3': [+1, 0, 0, 0, 63, 25],
  'I4': [-1, 0, 0, 0, 14, 7],
  'I5': [+1, 0, 0, 0, 23, 8],
  'I6': [-1, 0, 0, 0, 46, 51],
  'J':  [+1, 0, 0, 0, 37, 14]
}

def initial_memory_value(adr):
  return hash(str(adr)) % (64**5)

class VM3:
  def __init__(self):
    pass

  def execute(at = None, start = None):
    pass

  def load(mega):
    pass

  def state():
    """Returns MEGA hash"""
    return {
      0: [+1, 0, 0, 0, 0, 0],
      # ....................
      3999: [+1, 0, 0, 0, 0, 0],
      'A': [+1, 0, 0, 0, 0, 0],
      'X': [+1, 0, 0, 0, 0, 0],
      'I1': [+1, 0, 0, 0, 0, 0],
      'I2': [+1, 0, 0, 0, 0, 0],
      'I3': [+1, 0, 0, 0, 0, 0],
      'I4': [+1, 0, 0, 0, 0, 0],
      'I5': [+1, 0, 0, 0, 0, 0],
      'I6': [+1, 0, 0, 0, 0, 0],
      'J': [+1, 0, 0, 0, 0, 0],
      'CA': 3333,
      'CF': -1,
      'OF': 1,
      'HLT': 0
    }

class MathTestCase(unittest.TestCase):
  def setup(self):
    self.vm = TestedVirtualMachine()
    self.fillContext()
  
  def init(regs=None, memory=None):
    ctx = YetAnotherVMContext()
    ctx.memory = fill_memory_with_default_values()

    if memory is not None:
      self.vm.init_memory(memory)

      #for adr, value in memory.iteritems():
        #self.memory[adr] = value

    if regs is not None:
      ctx.regs = ctx.regs.merge(regs)

  def testADD(self):
    self.init(regs={'A': [+1, 0, 0, 0, 0, 0]}, memory={0: [+1, 0, 0, 0, 0, 1]})
    self.save_context()   # self.saved_context
    
    self.vm.execute_one_instruction(0)
  
    diff = self.compare_contexts(self.saved_context, self.context)
    self.assertEqual(diff, {
      'A': 1,
      'ca': 1
    })