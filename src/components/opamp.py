
""" A component that designates a opamp. """

from graph import Node, Edge

class Opamp(object):
    """ Opamp component """
    def __init__(self, graph, node_a=None, node_b=None, node_out=None):
        """ Initializes a opamp with two nodes.  A represents V- while B
        represents V+.

        node_out MUST HAVE SOURCE=TRUE

        If nodes / edges aren't supplied, new ones are created.
        Supplied nodes / edges should be part of the supplied graph.

        The assumption is that the op amp is powered with unlimited symmetric
        voltage rails so if you use it as a comparator you're going to
        have a bad time.

        NOTE TO USERS:
        This is the hackiest module in the program so listen closely.

        - We don't include the edges going into the op amp at the input nodes
            because they are always zero.
        - We have an output edge connected from the output node to an internal
            node.  The internal node is not added to the variables list
            because we don't care about it.  But the edge is in the list,
            in order to satisfy KCL constraints.  So consider edge_out to exist
            only to provide an extra degree of freedom at the output node.

        Example usage, here's a buffer:

        >>> graph = Graph()
        >>> node_out = Node(graph, source=True, output=True)
        >>> node_in = Node(graph, value=5, fixed=True)
        >>> op_amp = Opamp(graph, node_a=node_out, node_b=node_in, node_out=node_out)
        >>> graph.add_component(op_amp)
        >>> graph.solve()

        node_out.value() should be 5.

        Args:
            graph : Graph object
            node_a : Node object
            node_b : Node object
            node_out : Node object

        Returns:
            Opamp object
        """
        if not node_a:
            node_a = Node(graph)
        if not node_b:
            node_b = Node(graph)
        if not node_out:
            node_out = Node(graph)

        self._node_a = node_a
        self._node_b = node_b
        self._node_out = node_out

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

    def node_out(self):
        """ Returns output node.

        Returns:
            Node object
        """
        return self._node_out

    def variables(self):
        """ Returns a set of variables under constraints.

        Returns:
            set of Nodes, Edges, tuples, or strings
        """
        return set([self._node_a, self._node_b, self._node_out])

    def substitutions(self):
        """ Return a dictionary mapping each symbol to a value.  Return
            an empty dictionary if no substitutions exist

            Returns:
                dictionary from sympy variable to value
        """
        return {}

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
        alpha = 0.5

        # Constraint is alpha * (v_b - v_a) - v_out = 0
        #coefficients = [-alpha, alpha, -1]
        #variables = [self._node_a, self._node_b, self._node_out]

        #v_d = self._node_b.value() - self._node_a.value()
        #coefficients = [-1, alpha * v_d]
        #variables = [self._node_out, "1"]

        # TODO Ugly hack!  (This is not how op amps work.)
        coefficients = [1, -1]
        variables = [self._node_a, self._node_b]
        return [(coefficients, variables)]
