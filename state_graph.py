from state_description import *

# discretized quantity and derivative spaces
IQ_SPACE = [ZERO, POS]
ID_SPACE = [NEG, ZERO, POS]
VQ_SPACE = [ZERO, POS, MAX]
VD_SPACE = [NEG, ZERO, POS]
OQ_SPACE = [ZERO, POS, MAX]
OD_SPACE = [NEG, ZERO, POS]


def create_all_nodes():
    """
     For each possible state description, create a node.
     After this operation, the graph is totally disconnected.
    """

    # the graph is initially empty
    graph = {}

    # iterate over the entire state space
    for iq_val in IQ_SPACE:
        for id_val in ID_SPACE:
            for vq_val in VQ_SPACE:
                for vd_val in VD_SPACE:
                    for oq_val in OQ_SPACE:
                        for od_val in OD_SPACE:
                            # create new state description
                            sd = State_Description([iq_val, id_val,
                                                   vq_val, vd_val,
                                                   oq_val, od_val])

                            # add the new description to the graph as node
                            # the list of nodes reachable from the new node
                            # is empty for now
                            graph[sd] = []

    return graph



