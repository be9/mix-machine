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


class VM3:
    """ The main interface of abstract VM """
    def __init__(self):
        pass

    def execute(self, at = None, start = None):
        """ Runs 1 command at "at", or from "start" to "HLT" instruction and returns number of elapsed cycles """
        pass

    def load(self, mega):
        """ Loads initial state of VM form MEGA hash """
        pass

    def state(self):
        """ Returns state of VM in MEGA hash """
        return {}
