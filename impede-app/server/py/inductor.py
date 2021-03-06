
""" A component that designates a capacitor. """

import sympy as sy

from component import Component
from config import Config

class Inductor(Component):
    """ Inductor component """
    def __init__(self, graph, inductance, node_a, node_b, edge_i):
        """ Initializes a inductance with two nodes.  Current goes from
        A to B.  Supplied nodes / edges should be part of the supplied
        graph.

        Args:
            inductance : float
            graph : Graph object
            node_a : Node object
            node_b : Node object
            edge_i : Edge object

        Returns:
            Inductor object
        """
        self._node_a = node_a
        self._node_b = node_b
        self._edge_i = edge_i
        self._inductance = inductance

        self._i = sy.Symbol("i" + str(self))  # TODO better mangling

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
        return set([self._node_a, self._node_b, self._edge_i])

    def substitutions(self):
        """ Return a dictionary mapping each symbol to a value.  Return
            an empty dictionary if no substitutions exist

            Returns:
                dictionary from sympy variable to value
        """
        mappings = {}
        mappings[self._i] = self._edge_i.value()
        return mappings

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
        # Inductor equation
        cs = [float(-1) / self._inductance,
              float(1) / self._inductance,
              float(1) / Config.time_step]
        xs = [self._node_a, self._node_b, self._edge_i]
        b = self._i / Config.time_step

        constraint = Constraint(cs, xs, b)
        return [constraint]
