# global constants for qualitative state descriptions
ZERO = 0
POS = 1
NEG = -1
MAX = 2

IQ = 0
ID = 1
VQ = 2
VD = 3
OQ = 4
OD = 5

class State_Description:
    """
     A qualitative state description for a tub consisting of an inflow, volume,
     and outflow. Each of these features of the state has both a quantity and a
     derivative.

     The parameters of a state description are always given in the following
     order:
     inflow_q, inflow_d, volume_q, volume_d, outflow_q, outflow_d

     The parameters passed to State_Description should be (a list of) ints.
     Use the global constants defined above for best results.
    """

    # mapping of integer values of global constants to strings for printing
    str_trans = {0 : '0', 1 : '+', -1 : '-', 2 : 'MAX'}

    def __init__(self, values = 6 * [ZERO]):
        # sanitize input
        if len(values) != 6:
            values = 6 * [ZERO]
            print('Invalid state description: should be six ints')

        self.params = values

    def get_inflow_q(self):
        return self.params[IQ]

    def get_inflow_d(self):
        return self.params[ID]

    def get_volume_q(self):
        return self.params[VQ]

    def get_volume_d(self):
        return self.self.params[VD]

    def get_outflow_q(self):
        return self.self.params[OQ]

    def get_outflow_d(self):
        return self.params[OD]

    def get_all_params(self):
        return self.params

    def set_inflow_q(self, value):
        self.params[IQ] = value

    def set_inflow_d(self, value):
        self.params[ID] = value

    def set_volume_q(self, value):
        self.params[VQ] = value

    def set_volume_d(self, value):
        self.params[VD] = value

    def set_outflow_q(self, value):
        self.params[OQ] = value

    def set_outflow_d(self, value):
        self.params[OD] = value

    def set_all_params(self, values):
        # sanitize input
        if len(values) != 6:
            print('Invalid state description: should be six ints')
        else:
            self.params = values


    def __str__(self):
        string = 'STATE DESCRIPTION\n'

        string += 'INFLOW\n'
        string += 'Q: ' + State_Description.str_trans[self.params[IQ]] + '\n'
        string += 'd: ' + State_Description.str_trans[self.params[ID]] + '\n'

        string += 'VOLUME\n'
        string += 'Q: ' + State_Description.str_trans[self.params[VQ]] + '\n'
        string += 'd: ' + State_Description.str_trans[self.params[VD]] + '\n'

        string += 'OUTFLOW\n'
        string += 'Q: ' + State_Description.str_trans[self.params[OQ]] + '\n'
        string += 'd: ' + State_Description.str_trans[self.params[OD]] + '\n'

        return string

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (tuple(self.params) == tuple(other.params))
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(self.params))
