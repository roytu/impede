
""" Graph module that defines nodes, edges, and graphs.

Nodes and edges carry an ID that identifies them within the graph.
IDs should be a type that supports equality.
"""

from constraint import Problem
from config import Config as Cfg
from util import irangef

class Node(object):
    """ A node object designates each point in the graph.
    On initialization, the node is assigned an ID by the graph. """
    def __init__(self, graph, value=0, fixed=False):
        """ Adds this node to the graph and retrieves an ID.

        Args:
            graph : Graph object
            value : any type
        """
        self._id = graph.add_node(self)
        self._value = value
        self._fixed = fixed

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
        """ Sets the value stored by this node.

        Args:
            value : any type
        """
        self._value = value

class Edge(object):
    """ A edge object designates each current-carrying in the graph.
    On initialization, the edge is assigned an ID by the graph. """
    def __init__(self, graph, value=0, fixed=False):
        """ Adds this edge to the graph and retrieves an ID.

        Args:
            graph : Graph object
            value : any type
        """
        self._id = graph.add_edge(self)
        self._value = value
        self._fixed = fixed

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
        problem = Problem()

        # Initialize variables and supply domains (input voltages are fixed)
        res = 1

        # Gather variables
        variables = set([])
        for component in self._components:
            variables = variables.union(set(component.variables()))

        solution = None
        while not solution:
            problem = Problem()
            for component in self._components:
                # Add constraints
                constraints = component.constraints()
                for constraint in constraints:
                    problem.addConstraint(*constraint)

            for variable in variables:
                # If node is an input voltage, restrict domain
                if variable.is_fixed():
                    problem.addVariable(variable, [variable.value()])
                else:
                    if isinstance(variable, Node):
                        voltage_range = irangef(Cfg.min_voltage, Cfg.max_voltage, res)
                        problem.addVariable(variable, list(voltage_range))
                    if isinstance(variable, Edge):
                        current_range = irangef(Cfg.min_current, Cfg.max_current, res)
                        problem.addVariable(variable, list(current_range))

            # Run the constraint solver.  If there are no solutions, initialize with
            # finer domains and retry until we get a solution.
            solution = problem.getSolution()
            res *= Cfg.resolution_step

        # Apply the solution to the graph
        for variable, value in solution.items():
            variable.set_value(value)
