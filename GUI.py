import matplotlib.pyplot as plt
import networkx as nx
import pylab

class AnnoteFinder:
    """
    Callback for matplotlib to visit a node (display an annotation) when points
    are clicked on. The point which is closest to the click and within xtol and
    ytol is identified.
    http://www.scipy.org/Cookbook/Matplotlib/Interactive_Plotting
    The click updates the graph, by making the current node yellow and showing
    the intra and inter state information.
    """
    def __init__(self, xdata, ydata, annotes, axis=None, xtol=None, ytol=None):
        self.xdata = xdata
        self.ydata = ydata
        self.annotes = annotes
        if xtol is None: xtol = ((max(xdata) - min(xdata))/float(len(xdata)))/2
        if ytol is None: ytol = ((max(ydata) - min(ydata))/float(len(ydata)))/2
        self.xtol = xtol
        self.ytol = ytol
        if axis is None: axis = pylab.gca()
        self.axis= axis
        self.drawnAnnotations = {}
        self.links = []

    def __call__(self, event):
        ''' Callback function for the on click event. '''
        if event.inaxes:
            clickX = event.xdata
            clickY = event.ydata
            if self.axis is None or self.axis == event.inaxes:
                annotes = []
                data = zip(self.xdata, self.ydata, self.annotes)
                for x, y, a in data:
                    # Check if click is close to a node
                    if clickX-self.xtol < x < clickX+self.xtol and \
                            clickY-self.ytol < y < clickY+self.ytol:
                        dx, dy = x - clickX, y - clickY
                        annotes.append((dx*dx + dy*dy, x, y, a))
                if annotes:
                    # Select nearest node
                    annotes.sort()
                    distance, x, y, annote = annotes[0]
                    self.update_plot(annote)

    def set_graph_info(self, ax1, ax2, ax3, graph, pos, parent_nodes, end_nodes, node_labels):
        ''' The the plotting info, like axes, the graph etc. '''
        self.ax1 = ax1
        self.ax2 = ax2
        self.ax3 = ax3
        self.graph = graph
        self.pos = pos
        self.parent_nodes = parent_nodes
        self.end_nodes = end_nodes
        self.node_labels = node_labels

    def generate_inter_state(self, parent, child, quantity):
        ''' Generate the inter state information. '''
        if (quantity == "inflow"):
            pq = parent.get_inflow_q()
            cq = child.get_inflow_q()
            pd = parent.get_inflow_d()
            cd = child.get_inflow_d()
        elif (quantity == "volume"):
            pq = parent.get_volume_q()
            cq = child.get_volume_q()
            pd = parent.get_volume_d()
            cd = child.get_volume_d()
        elif (quantity == "outflow"):
            pq = parent.get_outflow_q()
            cq = child.get_outflow_q()
            pd = parent.get_outflow_d()
            cd = child.get_outflow_d()
        elif (quantity == "outflow"):
            pq = parent.get_outflow_q()
            cq = child.get_outflow_q()
            pd = parent.get_outflow_d()
            cd = child.get_outflow_d()
        elif (quantity == "height"):
            pq = parent.get_height_q()
            cq = child.get_height_q()
            pd = parent.get_height_d()
            cd = child.get_height_d()
        elif (quantity == "pressure"):
            pq = parent.get_pressure_q()
            cq = child.get_pressure_q()
            pd = parent.get_pressure_d()
            cd = child.get_pressure_d()
        text = ""
        if (pq == cq):
            text += "the q of the " + quantity + " did not change"
        elif (pq < cq):
            text += "the q of the " + quantity + " increased"
        elif (pq > cq):
            text += "the q of the " + quantity + " decreased"
        if (pd == cd):
            text += ", and the d of the " + quantity + " did not change"
        elif (pd < cd):
            text += ", and the d of the " + quantity + " increased"
        elif (pd > cd):
            text += ", and the d of the " + quantity + " descreased"

        return text

    def show_graph(self, selected_node):
        ''' Show the graph with yellow node a scurrent node. '''
        self.ax3.set_title('Select a state to see its value')
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=self.end_nodes, node_color='blue')
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=self.parent_nodes, node_color='red')
        nx.draw_networkx_nodes(self.graph, self.pos, nodelist=[selected_node], node_color='yellow')
        nx.draw_networkx_edges(self.graph, self.pos)
        nx.draw_networkx_labels(self.graph, self.pos, self.node_labels)

    def show_inter_state_info(self, node):
        ''' Show the inter state information below the table.
        (only works on full screen) '''
        x = 0.3
        y = -0.1
        text = ""
        for s in self.graph.predecessors(node):
            text += s.get_name() + ": \n"
            text += self.generate_inter_state(s, node, "inflow")
            text += "\n"
            text += self.generate_inter_state(s, node, "volume")
            text += "\n"
            text += self.generate_inter_state(s, node, "outflow")
            text += "\n"
            text += self.generate_inter_state(s, node, "height")
            text += "\n"
            text += self.generate_inter_state(s, node, "pressure")
            text += "\n"
        self.ax1.text(x, y, text)

    def show_table(self, description):
        ''' Show the value and derivative of the quantities in a table below
        the graph. '''
        magnitude = []
        derivative = []
        for i, p in enumerate(description.get_all_params()):
            if p == -1: p = '-'
            elif p == 1: p = '+'
            elif p == 2: p = 'MAX'

            if i % 2 == 0:
                magnitude.append(p)
            else:
                derivative.append(p)
        data = [magnitude, derivative]

        columns = ('INFLOW', 'VOLUME', 'OUTFLOW', 'HEIGHT', 'PRESSURE')
        rows = ['Q', 'd']

        self.ax2.table(cellText=data, rowLabels=rows, colLabels=columns,
                      loc='center', cellLoc='center')

    def update_plot(self, node):
        ''' Update the GUI after click. '''
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax1.axis('off')
        self.ax2.axis('off')
        self.ax3.axis('off')
        self.show_graph(node)
        self.show_inter_state_info(node)
        self.show_table(node)
        plt.gcf().canvas.draw_idle()


class StateVisualisation:
    def __init__(self, data):
        self.graph = nx.DiGraph()
        self.data = data
        self.visited = []
        self.state_map = {}

    def set_name(self, parent):
        ''' Recursively set the name of a state to s_n. '''
        if parent in self.state_map:
            parent.set_name(self.state_map[parent])
        else:
            parent.set_name('s' + str(len(self.state_map.keys())))
            self.state_map[parent] = parent.get_name()
        for child in self.data[parent]:
            self.set_name(child)

    def generate_graph(self, parent):
        ''' Recursively generate the graph by adding the edges between the
            parent node and its children. '''
        if parent in self.visited: return

        self.visited.append(parent)
        if parent in self.data.keys():
            for child in self.data[parent]:
                self.graph.add_edge(parent, child)
                self.generate_graph(child)

    def show_graph(self):
        ''' Show the graph as GUI. '''
        # Create 3 axes to show graph, state information and trace
        fig = plt.figure()
        ax1 = fig.add_subplot(313)
        ax2 = fig.add_subplot(312)
        ax3 = fig.add_subplot(311)
        ax3.set_title('Select a state to see its value')
        ax1.axis('off')
        ax2.axis('off')
        ax3.axis('off')

        # Create the graph and get positions of the node used for the on click
        pos = nx.spring_layout(self.graph)
        x, y, annotes = [],[],[]
        # Keep track of parent nodes that have children and end nodes that don't
        parent_nodes = []
        end_nodes = []
        for key in pos:
            if len([s for s in self.graph.successors(key)]) == 0:
                end_nodes.append(key)
            else:
                parent_nodes.append(key)
            d = pos[key]
            annotes.append(key)
            x.append(d[0])
            y.append(d[1])

        # Draw graph, blue is end node, red is parent node
        nx.draw_networkx_nodes(self.graph, pos, nodelist=end_nodes, node_color='blue')
        nx.draw_networkx_nodes(self.graph, pos, nodelist=parent_nodes, node_color='red')
        # Draw edges and labels
        nx.draw_networkx_edges(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos, self.state_map)

        # Callback class for onclick event
        af = AnnoteFinder(x, y, annotes)
        af.set_graph_info(ax1, ax2, ax3, self.graph, pos, parent_nodes,
                         end_nodes, self.state_map)
        fig.canvas.mpl_connect('button_press_event', af)

        # Uses tkagg, not sure if that's standard
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.show()

if __name__ == "__main__":
    main()
