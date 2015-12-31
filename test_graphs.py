
""" Module to test example graphs. """

from config import Config
from tests import test
from graph import Node, Edge, Graph
from wire import Wire
from resistor import Resistor
from common_filters import InvertingOpAmpFilter

def test_graphs():
    """ Test graphs. """
    # Simple wire
    graph = Graph()
    node_a = Node(graph, value=5, fixed=True)
    node_b = Node(graph, output=True)
    wire = Wire(graph, node_a, node_b)
    graph.add_component(wire)
    graph.solve()
    # Test that the voltage at both points is equal
    test(5, node_b.value(), epsilon=Config.epsilon)

    # Chained wires
    graph = Graph()
    node_a = Node(graph, value=10, fixed=True)
    node_b = Node(graph)
    node_c = Node(graph)
    node_d = Node(graph, output=True)

    wire = Wire(graph, node_a, node_b)
    graph.add_component(wire)

    wire = Wire(graph, node_b, node_c)
    graph.add_component(wire)

    wire = Wire(graph, node_c, node_d)
    graph.add_component(wire)

    graph.solve()

    # Test that the voltage at both points is equal
    test(10, node_d.value(), epsilon=Config.epsilon)

    # Simple resistor
    graph = Graph()
    node_a = Node(graph, value=5, fixed=True)
    node_b = Node(graph, value=0, fixed=True)
    edge_i = Edge(graph, node_a, node_b)
    resistor = Resistor(graph, 10, node_a, node_b, edge_i)
    graph.add_component(resistor)
    graph.solve()
    # Test that the current through the resistor is 0.5
    test(0.5, edge_i.value(), epsilon=Config.epsilon)

    # Inverting op amp
    filt = InvertingOpAmpFilter.make(100, 100)
    input_signal = [5]
    output_signal = filt.execute(input_signal)
    # Test that the op amp inverts the input voltage
    test(-input_signal[0], output_signal[0], epsilon=Config.epsilon)

if __name__ == "__main__":
    test_graphs()
