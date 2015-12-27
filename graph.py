
""" Graph module that defines nodes, edges, and graphs.

Nodes and edges carry an ID that identifies them within the graph.
IDs should be a type that supports equality.
"""

class Node(object):
    """ A node object designates each point in the graph.
    On initialization, the node is assigned an ID by the graph. """
    def __init__(self, graph, value=None):
        """ Adds this node to the graph and retrieves an ID.

        Args:
            graph : Graph object
            value : any type
        """
        self._id = graph.add_node(self)
        self._value = value

    def value(self):
        """ Returns the value stored by this node.

        Returns:
            any type
        """
        return self._value

class Edge(object):
    """ A edge object designates each current-carrying in the graph.
    On initialization, the edge is assigned an ID by the graph. """
    def __init__(self, graph, value=None):
        """ Adds this edge to the graph and retrieves an ID.

        Args:
            graph : Graph object
            value : any type
        """
        self._id = graph.add_edge(self)
        self._value = value

    def value(self):
        """ Returns the value stored by this node.

        Returns:
            any type
        """
        return self._value

class Graph(object):
    """ A graph object stores nodes and edges. """
    def __init__(self):
        self._nodes = []
        self._edges = []
        self._components = []

    def add_node(self, node):
        """ Adds a node to this graph and returns its ID.

        Args:
            node : Node object

        Returns:
            id (integer)
        """
        node_id = len(self._nodes)
        self._nodes.append(node)
        return node_id

    def add_edge(self, edge):
        """ Adds a edge to this graph and returns its ID.

        Args:
            edge : Edge object

        Returns:
            id (integer)
        """
        edge_id = len(self._edges)
        self._edges.append(edge)
        return edge_id

    def add_component(self, component):
        """ Adds the component to the component list. """
        self._components.append(component)

    def solve(self):
        """ Assigns values to nodes and edges until all constraints are met. """
        # TODO
        pass
