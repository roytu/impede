
""" Module to test example graphs. """

from config import Config
from tests import test
from graph import Node, Edge, Graph
from wire import Wire
from resistor import Resistor
from common_filters import InvertingOpAmpFilter
from opamp import Opamp

def test_wire():
    # Simple wire
    graph = Graph()
    node_a = Node(graph, value=5, fixed=True)
    node_b = Node(graph, output=True)
    wire = Wire(graph, node_a, node_b)
    graph.add_component(wire)
    graph.solve()
    # Test that the voltage at both points is equal
    return test(5, node_b.value(), epsilon=Config.epsilon)

def test_chained_wires():
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
    return test(10, node_d.value(), epsilon=Config.epsilon)

def test_resistor():
    """ Test graphs. """
    # Simple resistor
    graph = Graph()
    node_a = Node(graph, value=5, fixed=True)
    node_b = Node(graph, value=0, fixed=True)
    edge_i = Edge(graph, node_a, node_b)
    resistor = Resistor(graph, 10, node_a, node_b, edge_i)
    graph.add_component(resistor)
    graph.solve()
    # Test that the current through the resistor is 0.5
    return test(0.5, edge_i.value(), epsilon=Config.epsilon)

def test_buffer():
    # Buffer
    graph = Graph()
    node_out = Node(graph, output=True, source=True)
    node_in = Node(graph, value=5, fixed=True, source=True)
    op_amp = Opamp(graph, node_a=node_out, node_b=node_in, node_out=node_out)
    graph.add_component(op_amp)
    graph.solve()
    return test(5, node_out.value(), epsilon=Config.epsilon)

def test_inverting_opamp():
    # Inverting op amp
    filt = InvertingOpAmpFilter.make(100, 100)
    input_signal = [5]
    output_signal = filt.execute(input_signal)
    # Test that the op amp inverts the input voltage
    return test(-input_signal[0], output_signal[0], epsilon=Config.epsilon)

def test_all():
    tests = [test_wire, test_chained_wires, test_resistor, test_buffer,
             test_inverting_opamp]
    if False in [t() for t in tests]:
        print("At least one test failed.")
    else:
        print("All tests passed.")

if __name__ == "__main__":
    test_all()
