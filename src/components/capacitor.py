
""" A component that designates a capacitor. """

from graph import Node, Edge
from component import Component
from config import Config

class Capacitor(Component):
    """ Capacitor component """
    def __init__(self, graph, capacitance, node_a=None, node_b=None, edge_i=None):
        """ Initializes a capacitor with two nodes.  Current goes from
        A to B.  If nodes / edges aren't supplied, new ones are created.
        Supplied nodes / edges should be part of the supplied graph.

        Args:
            graph : Graph object
            capacitance : float
            node_a : Node object
            node_b : Node object
            edge_i : Edge object

        Returns:
            Capacitor object
        """
        if not node_a:
            node_a = Node(graph)
        if not node_b:
            node_b = Node(graph)
        if not edge_i:
            edge_i = Edge(graph, node_a, node_b)

        self._node_a = node_a
        self._node_b = node_b
        self._edge_i = edge_i
        self._capacitance = capacitance

    def node_a(self):
        """ Returns node A.

        Returns:
            Node object
        """
        return self._node_a

    def node_b(self):
        """ Returns node B.

        Returns:
            Node object
        """
        return self._node_b

    def edge_i(self):
        """ Returns the edge that stores current from A to B.

        Returns:
            Edge object
        """
        return self._edge_i

    def variables(self):
        """ Returns a set of variables under constraints.

        Returns:
            set of Nodes, Edges, tuples, or strings
        """
        return set([self._node_a, self._node_b, self._edge_i, "1"])

    def constraints(self):
        """ Returns a list of constraints that must be solved.
        A constraint is a tuple (coefficients, variables), where
        coefficients is a list of numbers corresponding to the linear
        equation:

            A_0 * x_0 + A_1 * x_1 + ... + A_{n-1} * x_{n-1} = 0,

        and variables is a list of the Node and Edge objects.

        Returns:
            List of tuples (coefficients, variables)
        """
        # Capacitor equation
        prev_voltage = self._node_a.value() - self._node_b.value()
        coefficient = [float(1) / Config.time_step,
                       float(-1) / Config.time_step,
                       float(-1) / self._capacitance,
                       float(-prev_voltage) / Config.time_step]
        variable = [self._node_a, self._node_b, self._edge_i, "1"]
        return [(coefficient, variable)]
