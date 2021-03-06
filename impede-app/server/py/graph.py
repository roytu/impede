
""" Graph module that defines nodes, edges, and graphs.

Nodes and edges carry an ID that identifies them within the graph.
IDs should be a type that supports equality.
"""

import numpy as np
from numpy import linalg
import sympy as sy
import scipy.sparse
from scipy.sparse.linalg import spsolve
from scipy.linalg import qr

from func import Func
from constraint import Constraint

class Node(object):
    """ A node object designates each point in the graph.
    On initialization, the node is assigned an ID by the graph. """
    def __init__(self, graph, value=0, fixed=False, output=False, source=False,
                 label=None):
        """ Adds this node to the graph and retrieves an ID.

        Args:
            graph : Graph object
            value : any type
            fixed : whether this node has a fixed voltage
            output : whether this is an output node
            source : whether this is a source or sink
            label : optional name for pretty printing
        """
        self._id = graph.add_node(self)
        self._value = value
        self._fixed = fixed
        self._output = output
        self._source = source
        self._label = label
        self._solution = None

    def is_fixed(self):
        """ Returns whether value is fixed or not.

        Returns:
            bool
        """
        return self._fixed

    def is_output(self):
        """ Returns whether this is an output node or not.  This matters
        because the graph assumes infinite impedence at output nodes.

        Returns:
            bool
        """
        return self._output

    def is_source(self):
        """ Returns whether this is a source or sink.  This matters
        because the graph does not run KCL on sources / sinks.

        Returns:
            bool
        """
        return self._source

    def value(self):
        """ Returns the value stored by this node.

        Returns:
            any type
        """
        return self._value

    def set_value(self, value):
        """ Sets the value stored by this node.

        Args:
            value : any type
        """
        self._value = value

    def __str__(self):
        if self._label:
            return self._label
        else:
            return object.__str__(self)

class Edge(object):
    """ A edge object designates each current-carrying in the graph.
    On initialization, the edge is assigned an ID by the graph. """
    def __init__(self, graph, node_a, node_b, value=0, fixed=False, label=None):
        """ Adds this edge to the graph and retrieves an ID.

        Args:
            graph : Graph object
            node_a : Node object
            node_b : Node object
            value : any type
            fixed : bool
            label : optional name for pretty printing
        """
        self._id = graph.add_edge(self)
        self._node_a = node_a
        self._node_b = node_b
        self._value = value
        self._fixed = fixed
        self._label = label

    def polarity(self, node):
        """ Returns the polarity wrt. the given node.  If the edge is incoming
        into the node, returns 1.  If the edge is outgoing from this node,
        returns -1.  Otherwise (if the node is not on this edge), return 0.

        Args:
            node : Node type

        Returns:
            1, 0, or -1
        """
        if node is self._node_b:
            return 1
        elif node is self._node_a:
            return -1
        else:
            return 0

    def is_fixed(self):
        """ Returns whether value is fixed or not.

        Returns:
            bool
        """
        return self._fixed

    def value(self):
        """ Returns the value stored by this node.

        Returns:
            any type
        """
        return self._value

    def set_value(self, value):
        """ Sets the value stored by this edge.

        Args:
            value : any type
        """
        self._value = value

    def __str__(self):
        if self._label:
            return self._label
        else:
            return object.__str__(self)

class Graph(object):
    """ A graph object stores nodes and edges. """
    def __init__(self):
        self._nodes = []
        self._edges = []
        self._components = []
        self.__sub_func = {}
        self.__variables = None

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

    def connected_edges(self, node):
        """ Given a node, return all edges touching this node, and their
        polarities.  Polarities are either 1 or -1, with 1 being an incoming
        edge and -1 being an outgoing edge.

        Args:
            node : Node object

        Returns:
            tuple ([edge], [polarity])
        """
        edges, polarities = [], []
        for edge in self._edges:
            polarity = edge.polarity(node)
            if polarity in (1, -1):
                edges.append(edge)
                polarities.append(polarity)
        return (edges, polarities)

    def variables(self):
        """ Return a list of variables to be used in the matrix solver.

        Returns:
            list of Nodes, Edges, or tuples
        """
        # TODO WARNING VARIABLES IS CACHED!!
        if self.__variables:
            return self.__variables

        # Gather variables and constraints
        variables = set([])
        for component in self._components:
            variables = variables.union(set(component.variables()))

        self.__variables = list(variables)
        return self.__variables

    def sympy_variables(self):
        """ Return a list of sympy variables associated with the variable
            variables in the order of the variable variables

        Returns:
            list of sympy symbols
        """
        return [var.value() for var in self.variables()
                if (isinstance(var, Node) or isinstance(var, Edge)) and
                    not isinstance(var.value(), sy.Float)]

    def constraints(self):
        """ Return a list of constraints to be used in the matrix solver.

        Returns:
            List of tuples (coefficients, variables)
        """
        const_var = "1"
        variables = self.variables()

        constraints = []
        for component in self._components:
            constraints += component.constraints()

        # Add constraints to fixed nodes
        for var in variables:
            if isinstance(var, Node) and var.is_fixed():
                cs = [1]
                xs = [var]
                b = var.value()

                constraints.append(Constraint(cs, xs, b))

        # Add KCL constraints
        for var in variables:
            if isinstance(var, Node):
                # Get all edges and their directions wrt. this node
                if not var.is_source():
                    edges, polarities = self.connected_edges(var)
                    cs = polarities
                    xs = edges
                    constraints.append(Constraint(cs, xs))
        return constraints

    def internal_subs(self):
        """ Return a dictionary of internal substitutions

            Returns:
                dictionary with mappings from sympy symbols to values
        """
        subs = {}
        for component in self._components:
            subs.update(component.substitutions())
        return subs

    def update(self, external_subs=None):
        """ Assumes nodes store the current value for this iteration, and
            updates all variables using this state.  Effectively runs one
            timestep.

            Args:
                external_subs: Mapping from sympy symbols to floats
                    (default=None)
        """
        variables = self.variables()

        # Get all substitutions
        subs = {}
        if external_subs:
            subs = external_subs.copy()  # TODO Optimization, don't copy
        subs.update(self.internal_subs())

        assignments = {}
        for var, expr in self._solution.items():
            # Store this in an intermediate dictionary
            assignments[var] = expr(subs)

        # Perform all assignments
        for var, value in assignments.items():
            var.set_value(value)

    def solve(self):
        """ Solves the matrix symbolically and stores a mapping between each
            hanging symbol and the expression to evaluate that updates
            that symbol.
        """
        # Gather variables and constraints
        variables = self.variables()
        constraints = self.constraints()

        # Allocate variables to rows
        var2row = dict()
        for i, var in enumerate(variables):
            var2row[var] = i

        # Determine size of matrix
        N = len(variables)
        A = sy.zeros(N, N)
        b = sy.zeros(N, 1)

        # Allocate each constraint to each row
        for i, cons in enumerate(constraints):
            # Build row one variable at a time
            row = sy.zeros(1, N)
            for c, x in zip(cons.cs, cons.xs):
                row[var2row[x]] = c

            # Add to matrix
            A[i, :] = row
            b[i] = cons.b

        # Solve the linear equation
        xs = A.LUsolve(b)
        self._solution = {}
        for var, expr in zip(variables, xs):
            if isinstance(var, Node) or isinstance(var, Edge):
                self._solution[var] = Func(expr)
