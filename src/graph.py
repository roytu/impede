
""" Graph module that defines nodes, edges, and graphs.

Nodes and edges carry an ID that identifies them within the graph.
IDs should be a type that supports equality.
"""

import numpy as np
from numpy import linalg
import scipy.sparse
from scipy.sparse.linalg import spsolve
from scipy.linalg import qr

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
            list of Nodes, Edges, tuples, or strings
        """
        const_variable = "1"
        # Gather variables and constraints
        variables = set([])
        for component in self._components:
            variables = variables.union(set(component.variables()))

        variables -= set([const_variable])
        variables = list(variables)
        variables.append(const_variable)
        return variables

    def constraints(self):
        """ Return a list of constraints to be used in the matrix solver.

        Returns:
            List of tuples (coefficients, variables)
        """
        const_variable = "1"
        variables = self.variables()

        constraints = []
        for component in self._components:
            constraints += component.constraints()
        #print("Component constraints: {0}".format(len(constraints)))

        # Add constraints to fixed nodes
        for variable in variables:
            if isinstance(variable, Node) and variable.is_fixed():
                new_constraint = ([1, -variable.value()], [variable, const_variable])
                constraints.append(new_constraint)
        #print("Fixed constraints: {0}".format(len(constraints)))

        # Add KCL constraints
        for variable in variables:
            if isinstance(variable, Node):
                # Get all edges and their directions wrt. this node
                edges, polarities = self.connected_edges(variable)
                if not variable.is_source():
                    if len(edges) <= 1:
                        if variable.is_output():
                            # Outputs assume an infinite impedence
                            new_constraint = ([1], edges)
                            constraints.append(new_constraint)
                    else:
                        new_constraint = (polarities, edges)
                        constraints.append(new_constraint)
        #print("KCL constraints: {0}".format(len(constraints)))

        # Add a constraint for the constant "1"
        constraints.append(([1], [const_variable]))
        # Note that this should be the last row in the matrix!!
        #print("All constraints: {0}".format(len(constraints)))

        return constraints

    def solve(self):
        """ Assigns values to nodes and edges until all constraints are met.
        TODO THIS CODE SUCKS
        """
        const_variable = "1"

        # Gather variables and constraints
        variables = self.variables()
        constraints = self.constraints()

        # For each constraint add a row to the matrix
        # Constraints take the form (coefficients, variables)
        var_to_row = dict()
        for i, variable in enumerate(variables):
            var_to_row[variable] = i

        dim = len(variables)
        constraint_matrix = np.zeros((dim, dim))

        for i, (cs, vs) in enumerate(constraints):
            row = np.zeros(dim)
            for c, v in zip(cs, vs):
                row[var_to_row[v]] = c
            constraint_matrix[i] = row

        # Solve the linear equation
        b = np.append(np.zeros(dim - 1), [1])
        solution = linalg.solve(constraint_matrix, b)

        # Apply the solution to the graph
        for variable, value in zip(variables, solution):
            if isinstance(variable, Node) or isinstance(variable, Edge):
                variable.set_value(value)
