from state_description import *
from collections import defaultdict

# discretized quantity and derivative spaces
IQ_SPACE = set([ZERO, POS])
ID_SPACE = set([NEG, ZERO, POS])
VQ_SPACE = set([ZERO, POS, MAX])
VD_SPACE = set([NEG, ZERO, POS])
OQ_SPACE = set([ZERO, POS, MAX])
OD_SPACE = set([NEG, ZERO, POS])


def find_neighbors(graph, to_search, sd):
    """
     Find all state descriptions which can be transitioned to from sd
     and add the appropriate edges to the graph.
    """

    params = sd.get_all_params()

    # check to see if the current state is stable (all derivs == ZERO)
    # if so, no further change is possible
    if ((((params[ID] == ZERO) and params[VD] == ZERO) and params[OD] == 0)):
        pass

    # initially, we consider any transition possible
    spaces = [IQ_SPACE.copy(), set([POS]),
              VQ_SPACE.copy(), VD_SPACE.copy(),
              OQ_SPACE.copy(), OD_SPACE.copy()]

    # prune transitions that don't respect influences
    spaces = enforce_influences(sd, spaces)

    # prune transitions that don't respect proportionality
    spaces = enforce_proportions(sd, spaces)

    # prune transitions where the new quantity doesn't
    # respect the current derivative
    spaces = enforce_derivatives(sd, spaces)

    # prune transitions that don't respect continuity
    spaces = enforce_continuity(sd, spaces)

    for iq_val in spaces[IQ]:
        for id_val in spaces[ID]:
            for vq_val in spaces[VQ]:
                for vd_val in spaces[VD]:
                    for oq_val in spaces[OQ]:
                        for od_val in spaces[OD]:
                            neighbor = State_Description([iq_val, id_val,
                                                                  vq_val, vd_val,
                                                                  oq_val, od_val])


                            # enforce correspondences from volume to outflow
                            # MAX outflow <=> MAX volume
                            # ZERO outflow <=> ZERO volume
                            if (((oq_val == MAX) == (vq_val == MAX))
                               and ((oq_val == ZERO) == (vq_val == ZERO))):

                                # if a quantity hits a max or min value,
                                # the corresponding derivative should level off
                                # e.g., ZERO inflow => ZERO change in inflow
                                if ((params[IQ] != POS) or (iq_val != ZERO)):
                                    id_val = ZERO
                                if ((params[VQ] != POS) or (vq_val != ZERO)):
                                    vd_val = ZERO
                                if ((params[VQ] != POS) or (vq_val != MAX)):
                                    vd_val = ZERO
                                if ((params[OQ] != POS) or (oq_val != ZERO)):
                                    od_val = ZERO
                                if ((params[OQ] != POS) or (oq_val != MAX)):
                                    od_val = ZERO

                                if neighbor == sd:
                                    continue
                                else:
                                    graph[sd] += [neighbor]
                                    to_search.append(neighbor)


def enforce_continuity(sd, spaces):
    """
     Eliminate transitions to states that don't preserve continuity.
     E.g., if the volume at one state is zero, you can't immediately
     transition to maximum volume at the next state.
    """
    params = sd.get_all_params()

    # there's no continuity to enforce on inflow quantity

    # the derivatives can't skip ZERO
    for i in [ID, VD, OD]:
        if params[i] == POS:
            spaces[i] = spaces[i].difference(set([NEG]))
        elif params[i] == NEG:
            spaces[i] = spaces[i].difference(set([POS]))

    # the quantity of volume and outflow can't skip POS
    for i in [VQ, OQ]:
        if params[i] == MAX:
            spaces[i] = spaces[i].difference(set([ZERO]))
        elif params[i] == ZERO:
            spaces[i] = spaces[i].difference(set([MAX]))

    return spaces

def enforce_influences(sd, spaces):
    """
     The derivative of volume in possible transitions is
     determined by the quantities of inflow and outflow.
    """

    params = sd.get_all_params()

    # inflow has a positive influence on volume
    inflow_influence = params[IQ]
    # outflow has a negative influence on volume
    outflow_influence = -1 * params[OQ]

    if inflow_influence == 0:
        if outflow_influence < 0:
            # the total influence on volume is negative
            spaces[VD] = set([NEG])
        else:
            # the total influence on volume is neutral
            spaces[VD] = set([ZERO])
    else:
        if outflow_influence == 0:
            # the total influence on volume is positive
            spaces[VD] = set([POS])

    # we cannot determine the total influence if inflow influence
    # is positive and outflow influence is negative

    return spaces

def enforce_proportions(sd, spaces):
    """
     The derivative of outflow in possible transitions is
     determined by the derivative of volume
    """

    params = sd.get_all_params()

    spaces[OD] = set([params[VD]])

    return spaces

def enforce_derivatives(sd, spaces):
    params = sd.get_all_params()

    if params[ID] == ZERO:
        spaces[IQ] = set([params[IQ]])

    for i in [VD, OD]:
        if params[i] == ZERO:
            # if derivative is ZERO, quantity can't change
            spaces[i - 1] = set([params[i - 1]])
        elif params[i] == POS:
            # if derivative is POS, quantity must stay same or increase
            if params[i - 1] != MAX:
                spaces[i - 1] = set([params[i - 1], params[i - 1] + 1])
            else:
                spaces[i - 1] = set([params[i - 1]])
        else:
            # if derivative is NEG, quantity must stay same or decrease
            if params[i - 1] != ZERO:
                spaces[i - 1] = set([params[i - 1], params[i - 1] - 1])
            else:
                spaces[i - 1] = set([params[i - 1]])

    return spaces

def main():

    # state transition graph
    graph = defaultdict(list)

    # describe an empty tub with no inflow
    empty = State_Description()
    # describe an empty tub in the instant the tap is opened
    tap_on = State_Description([ZERO, POS, ZERO, ZERO, ZERO, ZERO])

    # add an edge from empty to tap_on
    graph[empty] += [tap_on]

    # stack of nodes to search depth-first
    to_search = [tap_on]
    searched = [empty]

    while len(to_search) > 0:
        sd = to_search.pop()
        if sd not in searched:
            searched.append(sd)
            graph[sd] = []
            find_neighbors(graph, to_search, sd)

    print(len(graph.keys()))

    sd = State_Description([POS, ZERO, MAX, ZERO, MAX, ZERO])

    print(len(graph[sd]))
    for n in graph[sd]:
        print(n)


if __name__ == '__main__':
    main()



