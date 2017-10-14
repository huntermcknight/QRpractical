# global constants for qualitative state descriptions
ZERO = 0
POS = 1
NEG = -1
MAX = 2

class State_Description:
    """
     A qualitative state description for a tub consisting of an inflow, volume,
     and outflow. Each of these features of the state has both a quantity and a
     derivative.
    """

    # mapping of integer values of global constants to strings for printing
    str_trans = {0 : '0', 1 : '+', -1 : '-', 2 : 'MAX'}

    def __init__(self):
        self.inflow_q = ZERO
        self.inflow_d = ZERO

        self.volume_q = ZERO
        self.volume_d = ZERO

        self.outflow_q = ZERO
        self.outflow_d = ZERO

    def get_inflow_q(self):
        return self.inflow_q

    def get_inflow_d(self):
        return self.inflow_d

    def get_volume_q(self):
        return self.volume_q

    def get_volume_d(self):
        return self.volume_d

    def get_outflow_q(self):
        return self.outflow_q

    def get_outflow_d(self):
        return self.outflow_d

    def set_inflow_q(self, value):
        self.inflow_q = value

    def set_inflow_d(self, value):
        self.inflow_d = value

    def set_volume_q(self, value):
        self.volume_q = value

    def set_volume_d(self, value):
        self.volume_d = value

    def set_outflow_q(self, value):
        self.outflow_q = value

    def set_outflow_d(self, value):
        self.outflow_d = value

    def __str__(self):
        string = 'STATE DESCRIPTION\n'

        string += 'INFLOW\n'
        string += 'Q: ' + str_trans[self.inflow_q] + '\n'
        string += 'd: ' + str_trans[self.inflow_d] + '\n'

        string += 'VOLUME\n'
        string += 'Q: ' + str_trans[self.volume_q] + '\n'
        string += 'd: ' + str_trans[self.volume_d] + '\n'

        string += 'OUTFLOW\n'
        string += 'Q: ' + str_trans[self.outflow_q] + '\n'
        string += 'd: ' + str_trans[self.outflow_d] + '\n'

        return string

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
