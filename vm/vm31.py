from vm import VM
from vm_word import Word
from vm_memory import MEM_SIZE

from vm_memory import AddressOutOfRangeError
from vm_command import CommandNotFoundError
from vm_events import VMEvent, VMStop, VMHalt
from vm_errors import VMError, VMRuntimeError
from vm_command_parser import CommandInvalidIndexError, CommandInvalidFormatError

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'vm3'))
import vm3_errors

# MEGA hash:
#    { 0: [+1, 0, 0, 0, 0, 0],
#      # ....................
#      3999: [+1, 0, 0, 0, 0, 0],
#      'A': [+1, 0, 0, 0, 0, 0],
#      'X': [+1, 0, 0, 0, 0, 0],
#      'I1': [+1, 0, 0, 0, 0, 0],
#      'I2': [+1, 0, 0, 0, 0, 0],
#      'I3': [+1, 0, 0, 0, 0, 0],
#      'I4': [+1, 0, 0, 0, 0, 0],
#      'I5': [+1, 0, 0, 0, 0, 0],
#      'I6': [+1, 0, 0, 0, 0, 0],
#      'J': [+1, 0, 0, 0, 0, 0],
#      'CA': 0,
#      'CF': -1,
#      'OF': 0,
#      'HLT': 0
#    }

error_map = {   AddressOutOfRangeError      : vm3_errors.InvalidAddress,
                CommandInvalidIndexError    : vm3_errors.InvalidIndex,
                CommandInvalidFormatError   : vm3_errors.InvalidFieldSpec,
                CommandNotFoundError        : vm3_errors.UnknownInstruction,
                #InvalidCurAddrError     : vm3_errors.InvalidCA,
                #NegativeShiftError      : vm3_errors.NegativeShift,
                #InvalidMoveError        : vm3_errors.InvalidMove
            }

class VM31:
    """ The main interface of abstract VM """
    def __init__(self):
        self.vm = VM()

    def execute(self, at = None, start = None):
        """ Runs 1 command at "at", or from "start" to "HLT" instruction and returns number of elapsed cycles """
        assert( (at is not None) ^ (start is not None) )
        cycles = 0

        if at is not None:
            self.vm.context.rL = Word(at)

            try:
                cycles = self.vm.trace()
            except VMRuntimeError, e:
                raise error_map[type(e)]

        if start is not None:
            self.vm.context.rL = Word(start)

            try:
                while not self.vm.context.is_halted:
                    cycles += self.vm.trace()
            except VMRuntimeError, e:
                raise error_map[type(e)]

        
    def load(self, mega):
        """ Loads initial state of VM form MEGA hash """

        for addr, word in mega.items():
            if isinstance(addr, int):
                self.vm.context.mem[addr] = Word(word)

        if mega.get("A") is not None: self.vm.context.rA = Word(mega["A"])
        if mega.get("X") is not None: self.vm.context.rX = Word(mega["X"])
        if mega.get("J") is not None: self.vm.context.rJ = Word(mega["J"])
        if mega.get("CA") is not None: self.vm.context.rL = Word(mega["CA"])

        for i in (1,2,3,4,5,6):
            if mega.get("I" + str(i)) is not None: self.vm.context.rI[i] = Word(mega["I" + str(i)])

        if mega.get("CF") is not None: self.vm.context.CF = mega["CF"]
        if mega.get("OF") is not None: self.vm.context.OF = mega["OF"]
        if mega.get("HLT") is not None: self.vm.context.is_halted = bool(mega["HLT"])

    def state(self):
        """ Returns state of VM in MEGA hash """

        mega = dict([(str(i), self.vm.context.mem[i].get_bytes()) for i in xrange(0, MEM_SIZE)])

        mega["A"] = self.vm.context.rA.get_bytes()
        mega["X"] = self.vm.context.rX.get_bytes()
        mega["J"] = self.vm.context.rJ.get_bytes()
        mega["CA"] = self.vm.context.rL.get_bytes()

        for i in (1,2,3,4,5,6):
            mega["I" + str(i)] = self.vm.context.rI[i].get_bytes()

        mega["CF"] = self.vm.context.CF
        mega["OF"] = self.vm.context.OF
        mega["HLT"] = int(self.vm.context.is_halted)

        return mega
