from state_description import *
from plot_graph import PlotGraph
from GUI import StateVisualisation

# discretized quantity and derivative spaces
IQ_SPACE = [ZERO, POS]
VQ_SPACE = [ZERO, POS, MAX]
VD_SPACE = [NEG, ZERO, POS]

def determine_iq(params):
    """
     ([int]) -> [int]

     Choose plausible transitions for inflow based on the previous
     derivative of inflow.
    """
    # note that we can ignore continuity for inflow quantity since
    # it has only two possible values

    # if previous derivative was zero, new quantity stays constant
    if params[ID] == ZERO:
        iq_vals = [params[IQ]]
    # if previous derivative was positive, new quantity cannot decrease
    # note that ZERO is a point, so (ZERO, POS) must transition to (POS, POS)
    elif params[ID] == POS:
        iq_vals = [POS]
    # if previous derivative was negative, new quantity cannot increase
    else:
        iq_vals = IQ_SPACE[:IQ_SPACE.index(params[IQ]) + 1]

    return iq_vals

def determine_vq(params):
    """
     ([int]) -> [int]

     Choose plausible transitions for volume based on the previous
     derivative of volume.
    """
    # if previous derivative was zero, new quatity stays constant
    if params[VD] == ZERO:
        vq_vals = [params[VQ]]
    # if previous derivative was positive, new quantity cannot decrease
    elif params[VD] == POS:
        if params[VQ] == ZERO:
            # Zero is a point, so we must transition out
            vq_vals = [POS]
        elif params[VQ] == POS:
            vq_vals = [POS, MAX]
        else:
            vq_vals = [MAX]
    # if previous derivative was negative, new quantity cannot increase
    else:
        if params[VQ] == ZERO:
            vq_vals = [ZERO]
        elif params[VQ] == POS:
            vq_vals = [ZERO, POS]
        else:
            # MAX is a point, so we must transition out
            vq_vals = [POS]

    return vq_vals

def determine_vd(params, new_params):
    """
     ([int], [int]) -> [int]

     Choose plausible transitions for the derivative of volume based
     on positive influence of inflow and the negative influence of
     outflow.
    """
    # the derivative of volume depends positively on current inflow
    # quantity and negatively on the current outflow quantity

    # the derivative of volume is yet undetermined
    vd_determined = False

    if new_params[IQ] == ZERO:
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
                vd_vals = second_derivative_negative(params)
            elif params[OD] == ZERO:
                # second derivative cannot be determined, so
                # rely on continuity
                vd_vals = check_vd_continuity(params)
            else:
                # the second derivative is positive,
                # so the derivative must not decrease
                vd_vals = second_derivative_positive(params)
        elif params[ID] == POS:
            if params[OD] != POS:
                # the total influence on the derivative is positive
                vd_vals = second_derivative_positive(params)
            else:
                # second derivative cannot be determined, so
                # rely on continuity
                vd_vals = check_vd_continuity(params)
        else:
            if params[OD] != NEG:
                # the total influence on the derivative is negative
                vd_vals = second_derivative_negative(params)
            else:
                # second derivative cannot be determined, so
                # rely on continuity
                vd_vals = check_vd_continuity(params)
    else:
        # if vd was determined by inflow/outflow influence,
        # check that the proposed transition is continuous
        difference = vd_vals[0] - params[VD]
        if difference > 1 or difference < -1:
            vd_vals = []

    return vd_vals

def second_derivative_negative(params):
    """
     ([int]) -> [int]

     If the second derivative of volume is negative, transitions
     to non-increased first derivatives are possible.
    """
    if params[VD] == ZERO:
        # ZERO is a point, and we must transition out
        vd_vals = [NEG]
    elif params[VD] == POS:
        vd_vals = [ZERO, POS]
    else:
        vd_vals = [NEG]

    return vd_vals

def second_derivative_positive(params):
    """
     ([int]) -> [int]

     If the second derivative of volume is positive, transitions
     to non-decreased first derivatives are possible.
    """
    if params[VD] == ZERO:
        # ZERO is a point, so we must transition out
        vd_vals = [POS]
    elif params[VD] == POS:
        vd_vals = [POS]
    else:
        vd_vals = [NEG, ZERO]

    return vd_vals

def check_vd_continuity(params):
    """
     ([int]) -> [int]

     If the derivative of volume cannot be determined by first-order
     or second-order influences, just make sure the the transition
     is continuous with respect to the derivative of volume.
    """
    if params[VD] == ZERO:
        vd_vals = VD_SPACE
    elif params[VD] == POS:
        vd_vals = VD_SPACE[1:]
    else:
        vd_vals = VD_SPACE[:2]

    return vd_vals

def check_epsilon_ordering(params, new_params):
    """
     ([int], [int]) -> bool

     Check that instantaneous point transitions have occured before
     gradual interval transitions.
    """
    inflow_point = False
    volume_point = False

    epsilon_ordered = True

    if params[IQ] == ZERO and params[ID] == POS:
        if new_params[IQ] != POS or new_params[ID] != POS:
            epsilon_ordered = False
        inflow_point = True
    if params[VQ] == ZERO and params[VD] == POS:
        if new_params[VQ] != POS or new_params[VD] != POS:
            epsilon_ordered = False
        volume_point = True
    elif params[VQ] == MAX and params[VD] == NEG:
        if new_params[VQ] != POS or params[VD] != NEG:
            epsilon_ordered = False
        volume_point = True

    if inflow_point:
        if not volume_point and (new_params[VQ] != params[VQ]):
            epsilon_ordered = False
    if volume_point:
        if not inflow_point and (new_params[IQ] != params[IQ]):
            epsilon_ordered = False

    return epsilon_ordered

def check_plausibility(new_params):
    """
     ([int]) -> bool

     Check that a proposed state description is plausible.
     Any description proposed by find_neighbors is assumed
     to be plausible if it is not in this blacklist.
    """
    plausible = True

    # during the phase where inflow is increasing, volume shouldn't stabilize
    # in an interval
    if new_params == [POS, POS, POS, ZERO, POS, ZERO, POS, ZERO, POS, ZERO]:
        plausible = False
    # at the momemnt that inflow 'tops out', volume shouldn't already be
    # draining
    if new_params == [POS, ZERO, MAX, NEG, MAX, NEG, MAX, NEG, MAX, NEG]:
        plausible = False
    # at the moment that inflow 'tops out', volume shouldn't start draining
    # from an interval
    if new_params == [POS, ZERO, POS, NEG, POS, NEG, POS, NEG, POS, NEG]:
        plausible = False
    # should never reach a state where inflow is (ZERO, NEG)
    if new_params == [ZERO, NEG, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO, ZERO]:
        plausible = False
    if new_params == [ZERO, NEG, MAX, NEG, MAX, NEG, MAX, NEG, MAX, NEG]:
        plausible = False
    if new_params == [ZERO, NEG, POS, NEG, POS, NEG, POS, NEG, POS, NEG]:
        plausible = False
    # inflow shouldn't be completely stopped before the tub starts draining
    if new_params == [ZERO, ZERO, MAX, NEG, MAX, NEG, MAX, NEG, MAX, NEG]:
        plausible = False

    return plausible

def find_neighbors(graph, to_search, blacklist, sd, id_val):
    """
     Find all state descriptions which can be transitioned to from sd
     and add the appropriate edges to the graph.
    """
    # parameters of the current state
    params = sd.get_all_params()
    # parameters of the state being transitioned to
    new_params = [0] * 10
    new_params[ID] = id_val

    iq_vals = determine_iq(params)

    vq_vals = determine_vq(params)

    for iq_val in iq_vals:
        new_params[IQ] = iq_val
        for vq_val in vq_vals:
            # the pairwise bidirectional correspondence between the MAX
            # and ZERO values of volume, height, pressure, and outflow
            # means that volume quantity determines the quantities of these
            # other system values as well
            for i in range(2, 10, 2):
                new_params[i] = vq_val

            vd_vals = determine_vd(params, new_params)

            for vd_val in vd_vals:
                # the chain of proportional influences from derivative of
                # volume to derivative of height, from derivative of
                # height to derivative of pressure, and from derivative
                # of pressure to derivative of outflow means that
                # the derivative of volume determines each of these
                # other derivatives
                for i in range(3, 10, 2):
                    new_params[i] = vd_val

                # check epsilon ordering
                epsilon_ordered = check_epsilon_ordering(params, new_params)

                if not epsilon_ordered:
                    continue

                # There are some states that should not be possible, but
                # our algorithm isn't sophisticated enough to tell, so we have to
                # remove them ad-hoc.
                plausible = check_plausibility(new_params)

                if not plausible:
                    continue

                # After all that pruning, the state described by new_params
                # can truly be called a neighbor of the current state.
                # It only remains to show that the neighbor is neither equivalent
                # to the current state nor already related to it.
                neighbor = State_Description(new_params)

                if neighbor == sd:
                    continue
                else:
                    if neighbor not in graph[sd] and neighbor not in  blacklist:
                        # prevent oscillation between pairs of closely related states
                        if neighbor in graph.keys():
                            if sd in graph[neighbor]:
                                continue
                        # clunky syntax required to cope with mutable objects
                        graph[sd] += [State_Description(new_params.copy())]
                        to_search.append(State_Description(new_params.copy()))

def main():
    """
     Build a state transition graph for an initially empty tub with an
     exogenously determined parabolic increasing inflow.
    """
    # state transition graph
    graph = {}
    # describe an empty tub with no inflow in the instant the tap is turned on
    tap_on = State_Description([ZERO, POS] + 8 * [ZERO])

    # stack of nodes to search depth-first
    to_search = [tap_on]
    searched = []

    # Blacklist is meant to capture the notion of "phases" in graph construction.
    # We don't want states from the current part of the construction to point
    # backwards. This helps capture the parabolic shape we're after and prevent
    # oscillation between closely related states. In each phase, every known state
    # is either searchable or blacklisted.
    # Blacklist starts out empty in the first phase.
    blacklist = []

    # build a graph under the exogenous influence: inflow is increasing
    id_val = POS
    while len(to_search) > 0:
        sd = to_search.pop()
        if sd not in searched:
            searched.append(sd)
            if sd not in graph.keys():
                graph[sd] = []
            find_neighbors(graph, to_search, blacklist, sd, id_val)
    # describe a tub where all parameters are positive after the tap
    # has been turned on
    filling = State_Description(10 * [POS])

    # reset the search stack
    # let filling and its descendents be the frontier, and blacklist
    # ancestors of filing
    to_search = []
    searched = []
    blacklist = []
    for key in graph.keys():
        if key == filling or key in graph[filling]:
            to_search.append(key)
        else:
            blacklist.append(key)

    # build a graph under the exogenous influence: inflow becomes steady
    id_val = ZERO
    while len(to_search) > 0:
        sd = to_search.pop()
        if sd not in searched:
            searched.append(sd)
            if sd not in graph.keys():
                graph[sd] = []
            find_neighbors(graph, to_search, blacklist, sd, id_val)

    # reset the search stack
    # let all descendents of filling whose inflows are (POS, ZERO)
    # be in the new frontier; blacklist all others
    to_search = []
    searched = []
    blacklist = []
    for key in graph.keys():
        if key in graph[filling] and key.get_inflow_d() == ZERO:
            to_search.append(key)
        else:
            blacklist.append(key)

    # build a graph under the exogenous influence: inflow is decreasing
    id_val = NEG
    while len(to_search) > 0:
        sd = to_search.pop()
        if sd not in searched:
            searched.append(sd)
            if sd not in graph.keys():
                graph[sd] = []
            find_neighbors(graph, to_search, blacklist, sd, id_val)

    # reset the search stack to all states with negative inflows;
    # blacklist all others
    to_search = []
    searched = []
    blacklist = []
    for key in graph.keys():
        if key.get_inflow_d() == NEG:
            to_search.append(key)
        else:
            blacklist.append(key)

    # build a graph under the exogenous influence: inflow has stabilized to zero
    id_val = ZERO
    while len(to_search) > 0:
        sd = to_search.pop()
        if sd not in searched:
            searched.append(sd)
            if sd not in graph.keys():
                graph[sd] = []
            find_neighbors(graph, to_search, blacklist, sd, id_val)

    print('The state graph generated by our model contains ' + str(len(graph.keys())) + ' distinct states.')

    print('See the state graph in state_graph.png.')
    dot_graph = PlotGraph(graph)
    dot_graph.generate_graph(tap_on)
    dot_graph.save()

    dot_graph = StateVisualisation(graph)
    dot_graph.set_name(tap_on)
    dot_graph.generate_graph(tap_on)
    dot_graph.show_graph()

if __name__ == '__main__':
    main()
