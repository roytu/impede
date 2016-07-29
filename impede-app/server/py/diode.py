
""" A component that designates a diode. """

import numpy as np
import sympy as sy

from constraint import Constraint

class Diode(object):
    """ Diode component """
    def __init__(self, graph, node_a, node_b, edge_i):
        """ Initializes a diode with two nodes.  Current goes from
        A to B.  Supplied nodes / edges should be part of the supplied
        graph.

        Args:
            graph : Graph object
            node_a : Node object
            node_b : Node object
            edge_i : Edge object

        Returns:
            Diode object
        """
        self._node_a = node_a
        self._node_b = node_b
        self._edge_i = edge_i

        self._dv = sy.Symbol("dv" + str(self))  # TODO better name mangling

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
            set of Nodes, Edges
        """
        return set([self._node_a, self._node_b, self._edge_i])

    def substitutions(self):
        """ Return a dictionary mapping each symbol to a value.  Return
            an empty dictionary if no substitutions exist

            Returns:
                dictionary from sympy variable to value
        """
        mappings = {}
        mappings[self._dv] = self._node_a.value() - self._node_b.value()
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
        """
        Taylor-expanding the Schottky equation to two terms gives:

            I_d = [I_s * (e^{V_d'} + 1)] + [I_s * (e^{V_d'} / nV_T)] V_D

        which is the constraint we are using here
        """
        #i_s = 10 ** -12
        i_s = 10 ** -6
        nvt = 0.026 * 0.3 / 0.65
        v_d = self._dv

        # Thresholding
        #THRES = 1
        #v_d = THRES if v_d > THRES else -THRES if v_d < -THRES else v_d

        c_0 = i_s * (sy.exp(v_d / nvt) - (v_d / nvt) * sy.exp(v_d / nvt) + 1)
        c_1 = i_s * sy.exp(v_d / nvt) / nvt

        # Overflow handling
        #THRES = 1000
        #c_0 = THRES if c_0 > THRES else -THRES if c_0 < -THRES else c_0
        #c_1 = THRES if c_1 > THRES else -THRES if c_1 < -THRES else c_1

        # Constraint is C_0 + C_1 * A - C_1 * B - I_D = 0
        cs = [c_1, -c_1, -1]
        xs = [self._node_a, self._node_b, self._edge_i]
        b = -c_0

        constraint = Constraint(cs, xs, b)
        return [constraint]
