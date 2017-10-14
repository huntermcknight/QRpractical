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

    def __init__(self, values = 6 * [ZERO]):

        # sanitize input
        if len(values) != 6:
            values = 6 * [ZERO]

        self.inflow_q = values[0]
        self.inflow_d = values[1]

        self.volume_q = values[2]
        self.volume_d = values[3]

        self.outflow_q = values[4]
        self.outflow_d = values[5]

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
        string += 'Q: ' + State_Description.str_trans[self.inflow_q] + '\n'
        string += 'd: ' + State_Description.str_trans[self.inflow_d] + '\n'

        string += 'VOLUME\n'
        string += 'Q: ' + State_Description.str_trans[self.volume_q] + '\n'
        string += 'd: ' + State_Description.str_trans[self.volume_d] + '\n'

        string += 'OUTFLOW\n'
        string += 'Q: ' + State_Description.str_trans[self.outflow_q] + '\n'
        string += 'd: ' + State_Description.str_trans[self.outflow_d] + '\n'

        return string

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.inflow_q == other.inflow_q
                    and self.inflow_d == other.inflow_d
                    and self.volume_q == other.volume_q
                    and self.volume_d == other.volume_d
                    and self.outflow_q == other.outflow_q
                    and self.outflow_d == other.outflow_d)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.inflow_q, self.inflow_d,
                     self.volume_q, self.volume_d,
                     self.outflow_q, self.outflow_d))
