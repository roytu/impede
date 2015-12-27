
""" Module to test example graphs. """

from config import Config
from tests import test
from graph import Node, Graph
from wire import Wire

def test_graphs():
    """ Test graphs. """
    # Simple wire
    graph = Graph()
    node_a = Node(graph)
    node_b = Node(graph)
    wire = Wire(graph, node_a, node_b)
    graph.add_component(wire)
    graph.solve()
    # Test that the voltage at both points is equal
    test(node_a, node_b, epsilon=Config.epsilon)

if __name__ == "__main__":
    test_graphs()
