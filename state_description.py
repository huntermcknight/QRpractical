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
HQ = 6
HD = 7
PQ = 8
PD = 9

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

    def __init__(self, values = 10 * [ZERO]):
        # sanitize input
        if len(values) != 10:
            values = 10 * [ZERO]
            print('Invalid state description: should be ten ints')

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

    def get_height_q(self):
        return self.self.params[HQ]

    def get_height_d(self):
        return self.params[HD]

    def get_pressure_q(self):
        return self.self.params[PQ]

    def get_pressure_d(self):
        return self.params[PD]

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

    def set_height_q(self, value):
        self.params[HQ] = value

    def set_height_d(self, value):
        self.params[HD] = value

    def set_pressure_q(self, value):
        self.params[PQ] = value

    def set_pressure_d(self, value):
        self.params[PD] = value

    def set_all_params(self, values):
        # sanitize input
        if len(values) != 10:
            print('Invalid state description: should be ten ints')
        else:
            self.params = values


    def __str__(self):
        # This pretty-print looks the nicest in stdout, but it doesn't align right
        # at all in graphviz prints. The commented-out string format looks okay in
        # graphviz, but it's still crooked for some nodes in the graph.

        header = '{: >2}{: ^8}{: ^8}{: ^9}{: ^8}{: ^10}'.format(' ', 'INFLOW', 'VOLUME', 'OUTFLOW', 'HEIGHT', 'PRESSURE')
        # string = 'INFLOW\t\tVOLUME\tOUTFLOW\tHEIGHT\t\tPRESSURE\n'

        quant_string = '{: >2}{: ^8}{: ^8}{: ^9}{: ^8}{: ^10}'.format('Q:', State_Description.str_trans[self.params[IQ]],
                                                                      State_Description.str_trans[self.params[VQ]],
                                                                      State_Description.str_trans[self.params[OQ]],
                                                                      State_Description.str_trans[self.params[HQ]],
                                                                      State_Description.str_trans[self.params[PQ]])
        # string += 'Q: ' + State_Description.str_trans[self.params[IQ]] + '\t\t\t'
        # string += 'Q: ' + State_Description.str_trans[self.params[VQ]] + '\t\t\t'
        # string += 'Q: ' + State_Description.str_trans[self.params[OQ]] + '\t\t\t'
        # string += 'Q: ' + State_Description.str_trans[self.params[HQ]] + '\t\t\t'
        # string += 'Q: ' + State_Description.str_trans[self.params[PQ]] + '\n'

        deriv_string = '{: >2}{: ^8}{: ^8}{: ^9}{: ^8}{: ^10}'.format('d:', State_Description.str_trans[self.params[ID]],
                                                                      State_Description.str_trans[self.params[VD]],
                                                                      State_Description.str_trans[self.params[OD]],
                                                                      State_Description.str_trans[self.params[HD]],
                                                                      State_Description.str_trans[self.params[PD]])
        # string += 'd: ' + State_Description.str_trans[self.params[ID]] + '\t\t\t'
        # string += 'd: ' + State_Description.str_trans[self.params[VD]] + '\t\t\t'
        # string += 'd: ' + State_Description.str_trans[self.params[OD]] + '\t\t\t'
        # string += 'd: ' + State_Description.str_trans[self.params[HD]] + '\t\t\t'
        # string += 'd: ' + State_Description.str_trans[self.params[PD]] + '\n'

        string = header + '\n' + quant_string + '\n' + deriv_string

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
