from vm_word import Word, MAX_WORD
from vm_errors import VMError, VMRuntimeError

class Add:
    """ Knuth int adition with overflov, if result is zero keeps the sign of op1 """
    def __init__(self, op1, op2):
        self.op1 = Word(op1)
        self.op2 = Word(op2)
        self.ov = 0

        int_res = int(self.op1) + int(self.op2)
        sign = 1 if int_res >= 0 else -1     # how to take sign(x) !?

        ov_test, int_res = divmod(abs(int_res), MAX_WORD+1)
        int_res *= sign
            
        self.res = Word(int_res)

        if ov_test != 0:
            self.ov = 1

        if int_res == 0:
            self.res.sign(self.op1.sign())


class Sub:
    """ Knuth int substraction with overflov, if result is zero keeps the sign of op1 """

    def __init__(self, op1, op2):
        self.op1 = Word(op1)
        self.op2 = Word(op2)
        self.ov = 0

        int_res = int(self.op1) - int(self.op2)
        sign = 1 if int_res >= 0 else -1     # how to take sign(x) !?

        ov_test, int_res = divmod(abs(int_res), MAX_WORD+1)
        int_res *= sign
            
        self.res = Word(int_res)

        if ov_test != 0:
            self.ov = 1

        if int_res == 0:
            self.res.sign(self.op1.sign())
