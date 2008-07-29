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

class Mul:
    """ Knuth int multiplication result have parts res_h and res_l with equal signs """

    def __init__(self, op1, op2):
        self.op1 = Word(op1)
        self.op2 = Word(op2)
        self.ov = 0

        int_res = int(self.op1) * int(self.op2)
        sign = 1 if int_res >= 0 else -1     # how to take sign(x) !?

        int_h, int_l = divmod(abs(int_res), MAX_WORD+1)
    
        self.res_h = Word(int(int_h))
        self.res_h.sign(sign)
        self.res_l = Word(int(int_l))
        self.res_l.sign(sign)

class Div:
    """ Knuth int division op1 have parts op1_h and op1_l with sign of op1_h """

    def __init__(self, op1_h, op1_l, op2):
        self.op1_h = Word(op1_h)
        self.op1_l = Word(op1_l)
        self.op2 = Word(op2)

        self.res_q = Word(0)
        self.res_r = Word(0)
            
        self.ov = 0

        int_op2 = int(self.op2)
        if int_op2 == 0:
            self.ov = 1
            
        else:
            sign = self.op1_h.sign() * self.op2.sign()
            
            int_op1 = abs(int(self.op1_h)) * (MAX_WORD+1)
            int_op1 += abs(int(self.op1_l))
            int_op1 *= self.op1_h.sign()

            int_q, int_r  = divmod(int_op1, int_op2)

            if int_q > MAX_WORD:
                self.ov = 1

            else:
                self.res_q = Word(int_q * sign)
                self.res_r = Word(int_r * self.op1_h.sign())    # Knuth division %)
