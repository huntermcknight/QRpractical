'''
Caitlin Lagrand
Create a state graph.
'''

import pydot

class PlotGraph:
    def __init__(self, qr_graph):
        self.dot_graph = pydot.Dot(graph_type="digraph")
        self.qr_graph = qr_graph
        self.visited = []

    def draw(self, parent_name, child_name):
        ''' Draw an edge betweeen the parent and child nodes. '''
        edge = pydot.Edge(str(parent_name), str(child_name))
        self.dot_graph.add_edge(edge)

    def generate_graph(self, parent):
        ''' Given the parent node, generate the children recursively. '''
        if parent in self.visited: return

        self.visited.append(parent)
        for child in self.qr_graph[parent]:
            self.draw(parent, child)
            self.generate_graph(child)

    def save(self):
        ''' Save the graph as png file. '''
        self.dot_graph.write_png('state_graph.png')
