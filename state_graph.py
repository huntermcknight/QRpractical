from state_description import *
from plot_graph import PlotGraph

# discretized quantity and derivative spaces
IQ_SPACE = [ZERO, POS]
VQ_SPACE = [ZERO, POS, MAX]
VD_SPACE = [NEG, ZERO, POS]


def find_neighbors(graph, to_search, sd, id_val):
    """
     Find all state descriptions which can be transitioned to from sd
     and add the appropriate edges to the graph.
    """
    # parameters of the current state
    params = sd.get_all_params()
    # parameters of the state being transitioned to
    new_params = [0] * 10
    new_params[ID] = id_val

    # possible inflow quantities are determined only by the previous
    # inflow derivative

    # note that we can ignore continuity for inflow quantity since
    # it has only two possible values

    # if previous derivative was zero, new quatity stays constant
    if params[ID] == ZERO:
        iq_vals = [params[IQ]]
    # if previous derivative was positive, new quantity cannot decrease
    elif params[ID] == POS:
        iq_vals = IQ_SPACE[IQ_SPACE.index(params[IQ]):]
    # if previous derivative was negative, new quantity cannot increase
    else:
        iq_vals = IQ_SPACE[:IQ_SPACE.index(params[IQ]) + 1]

    # similarly, volume quantities are determined only by the previous
    # volume derivative, but now continuity is a factor

    # if previous derivative was zero, new quatity stays constant
    if params[VD] == ZERO:
        vq_vals = [params[VQ]]
    # if previous derivative was positive, new quantity cannot decrease
    elif params[VD] == POS:
        vq_index = VQ_SPACE.index(params[VQ])
        if vq_index < 2:
            vq_vals = VQ_SPACE[vq_index: vq_index + 2]
        else:
            vq_vals = [VQ_SPACE[vq_index]]
    # if previous derivative was negative, new quantity cannot increase
    else:
        vq_index = VQ_SPACE.index(params[VQ])
        if vq_index > 0:
            vq_vals = VQ_SPACE[vq_index -1: vq_index + 1]
        else:
            vq_vals = [VQ_SPACE[vq_index]]

    for iq_val in iq_vals:
        new_params[IQ] = iq_val
        for vq_val in vq_vals:
            # the pairwise bidirectional correspondence between the MAX
            # and ZERO values of volume, height, pressure, and outflow
            # means that volume quantity determines the quantity of these
            # other system values as well
            for i in range(2, 10, 2):
                new_params[i] = vq_val

            # the derivative of volume depends positively on current inflow
            # quantity and negatively on the current outflow quantity

            # the derivative of volume is yet undetermined
            vd_determined = False

            if iq_val == ZERO:
                if new_params[OQ] > ZERO:
                    # the total influence on volume is negative
                    vd_vals = [NEG]
                    vd_determined = True
                else:
                    # the total influence on volume is neutral
                    vd_vals = [ZERO]
                    vd_determined = True
            else:
                if new_params[OQ] == ZERO:
                    # the total influence on volume is positive
                    vd_vals = [POS]
                    vd_determined = True

            # If inflow and outflow are both positive (or max),
            # the derivative of volume is qualitatively undetermined
            # by their influence

            if not vd_determined:
                # check that the second-derivative effects of inflow
                # and outflow influence on volume are consistent
                if params[ID] == ZERO:
                    if params[OD] == POS:
                        # the second derivative is negative,
                        # so the derivative must not increase
                        vd_index = VD_SPACE.index(params[VD])
                        if vd_index > 0:
                            vd_vals = VD_SPACE[vd_index -1: vd_index + 1]
                        else:
                            vd_vals = [VD_SPACE[vd_index]]
                    elif params[OD] == ZERO:
                        # the second derivative is neutral,
                        # so the derivative must not change
                        vd_vals = [params[VD]]
                    else:
                        # the second derivative is positive,
                        # so the derivative must not decrease
                        vd_index = VD_SPACE.index(params[VD])
                        if vd_index < 2:
                            vd_vals = VD_SPACE[vd_index: vd_index + 2]
                        else:
                            vd_vals = [VD_SPACE[vd_index]]
                elif params[ID] == POS:
                    if params[OD] != POS:
                        # the total influence on the derivative is positive
                        vd_index = VD_SPACE.index(params[VD])
                        if vd_index < 2:
                            vd_vals = VD_SPACE[vd_index: vd_index + 2]
                        else:
                            vd_vals = [VD_SPACE[vd_index]]
                    else:
                        # second derivative cannot be determined, so
                        # rely on continuity
                        if params[VD] == ZERO:
                            vd_vals = VD_SPACE
                        elif params[VD] == POS:
                            vd_vals = VD_SPACE[1:]
                        else:
                            vd_vals = VD_SPACE[:2]
                else:
                    if params[OD] != NEG:
                        # the total influence on the derivative is negative
                        vd_index = VD_SPACE.index(params[VD])
                        if vd_index > 0:
                            vd_vals = VD_SPACE[vd_index -1: vd_index + 1]
                        else:
                            vd_vals = [VD_SPACE[vd_index]]
                    else:
                        # second derivative cannot be determined, so
                        # rely on continuity
                        if params[VD] == ZERO:
                            vd_vals = VD_SPACE
                        elif params[VD] == POS:
                            vd_vals = VD_SPACE[1:]
                        else:
                            vd_vals = VD_SPACE[:2]

            for vd_val in vd_vals:
                # the chain of proportional influences from derivative of
                # volume to derivative of height, from derivative of
                # height to derivative of pressure, and from derivative
                # of pressure to derivative of outflow means that
                # the derivative of volume determines each of these
                # other derivatives
                for i in range(3, 10, 2):
                    new_params[i] = vd_val

                neighbor = State_Description(new_params)

                # There are some states that are apparently considered
                # impossible in DynaLearn that seem perfectly plausible
                # this algorithm (and often also to me). For the sake of
                # agreement with our DynaLearn model, it's necessary to
                # remove these states in an ugly and ad-hoc way.
                if new_params == [POS, POS, POS, ZERO, POS, ZERO, POS, ZERO, POS, ZERO]:
                    continue
                # if new_params == [POS, POS, MAX, NEG, MAX, NEG, MAX, NEG, MAX, NEG]:
                #     continue
                if new_params == [POS, ZERO, ZERO, POS, ZERO, POS, ZERO, POS, ZERO, POS]:
                    continue
                if new_params == [POS, ZERO, MAX, NEG, MAX, NEG, MAX, NEG, MAX, NEG]:
                    continue
                if new_params == [POS, ZERO, POS, NEG, POS, NEG, POS, NEG, POS, NEG]:
                    continue
                if new_params == [POS, NEG, ZERO, POS, ZERO, POS, ZERO, POS, ZERO, POS]:
                    continue
                if new_params == [ZERO, NEG, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO]:
                    continue
                if new_params == [ZERO, NEG, MAX, NEG, MAX, NEG, MAX, NEG, MAX, NEG]:
                    continue
                if new_params == [ZERO, NEG, POS, NEG, POS, NEG, POS, NEG, POS, NEG]:
                    continue
                if new_params == [ZERO, ZERO, MAX, NEG, MAX, NEG, MAX, NEG, MAX, NEG]:
                    continue

                if neighbor == sd:
                    continue
                else:
                    if neighbor not in graph[sd]:
                        # prevent oscillation between closely related states
                        if neighbor in graph.keys():
                            if sd in graph[neighbor]:
                                continue
                        # clunky syntax required to cope with mutable objects
                        graph[sd] += [State_Description(new_params.copy())]
                        to_search.append(State_Description(new_params.copy()))

def main():

    # state transition graph
    graph = {}
    # describe an empty tub with no inflow in the instant the tap is turned on
    tap_on = State_Description([ZERO, POS] + 8 * [ZERO])

    # stack of nodes to search depth-first
    to_search = [tap_on]
    searched = []

    # build a graph under the exogenous influence: inflow is increasing
    id_val = POS
    while len(to_search) > 0:
        sd = to_search.pop()
        if sd not in searched:
            searched.append(sd)
            if sd not in graph.keys():
                graph[sd] = []
            find_neighbors(graph, to_search, sd, id_val)

    # describe a tub where all parameters are positive after the tap
    # has been turned on
    filling = State_Description(10 * [POS])

    # reset the search stack
    to_search = [filling]
    for n in graph[filling]:
        to_search += [State_Description(n.get_all_params().copy())]
    searched = []

    # build a graph under the exogenous influence: inflow becomes steady
    id_val = ZERO
    while len(to_search) > 0:
        sd = to_search.pop()
        if sd not in searched:
            searched.append(sd)
            if sd not in graph.keys():
                graph[sd] = []
            find_neighbors(graph, to_search, sd, id_val)

    # reset the search stack to the descendents of the filling node whose
    # inflows are (pos, zero); these are the states which may transition to
    # inflow (pos, neg), which is the next step
    to_search = []
    searched = []
    for n in graph[filling]:
        if n.get_inflow_d() == ZERO:
            to_search.append(n)

    # build a graph under the exogenous influence: inflow is decreasing
    id_val = NEG
    while len(to_search) > 0:
        sd = to_search.pop()
        if sd not in searched:
            searched.append(sd)
            if sd not in graph.keys():
                graph[sd] = []
            find_neighbors(graph, to_search, sd, id_val)

    # reset the search stack to the descendents of the descendents of
    # the filling node whose inflows are (pos, neg)
    to_search = []
    searched = []
    for n1 in graph[filling]:
        for n2 in graph[n1]:
            if n2.get_inflow_d() == NEG:
                if n2 not in to_search:
                    to_search.append(n2)

    # build a graph under the exogenous influence: inflow has stabilized to zero
    id_val = ZERO
    while len(to_search) > 0:
        sd = to_search.pop()
        if sd not in searched:
            searched.append(sd)
            if sd not in graph.keys():
                graph[sd] = []
            find_neighbors(graph, to_search, sd, id_val)

    sd = State_Description([POS, ZERO] + 4 * [MAX, 0])

    print(len(graph.keys()))

    # for key in graph.keys():
    #     print(key)

    dot_graph = PlotGraph(graph)
    dot_graph.generate_graph(tap_on)
    dot_graph.save()


if __name__ == '__main__':
    main()
