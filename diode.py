
""" A component that designates a diode. """

import numpy as np

from graph import Node, Edge
from component import Component

class Diode(Component):
    """ Diode component """
    def __init__(self, graph, node_a=None, node_b=None, edge_i=None):
        """ Initializes a diode with two nodes.  Current goes from
        A to B.  If nodes / edges aren't supplied, new ones are created.
        Supplied nodes / edges should be part of the supplied graph.

        Args:
            graph : Graph object
            node_a : Node object
            node_b : Node object
            edge_i : Edge object

        Returns:
            Diode object
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
        """
        Taylor-expanding the Schottky equation to two terms gives:

            I_d = [I_s * (e^{V_d'} + 1)] + [I_s * (e^{V_d'} / nV_T)] V_D

        which is the constraint we are using here
        """
        i_s = 10 ** -12
        nvt = 0.026
        v_d = self._node_a.value() - self._node_b.value()

        THRES = 1
        v_d = THRES if v_d > THRES else -THRES if v_d < -THRES else v_d

        c_0 = i_s * (np.exp(v_d / nvt) - (v_d / nvt) * np.exp(v_d / nvt) + 1)
        c_1 = i_s * np.exp(v_d / nvt) / nvt

        # Overflow handling
        #THRES = 1000
        #c_0 = THRES if c_0 > THRES else -THRES if c_0 < -THRES else c_0
        #c_1 = THRES if c_1 > THRES else -THRES if c_1 < -THRES else c_1

        # Constraint is C_0 + C_1 * A - C_1 * B - I_D = 0
        coefficients = [c_1, -c_1, -1, c_0]
        variables = [self._node_a, self._node_b, self._edge_i, "1"]
        return [(coefficients, variables)]
