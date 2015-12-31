
""" Module that contains some example filters """

from graph import Node, Edge, Graph
from resistor import Resistor
from capacitor import Capacitor
from diode import Diode
from opamp import Opamp
from units import Units
from filter import Filter

def make_mxr_distortion_filter():
    """ Return the MXR filter from:

        http://www.premierguitar.com/articles/mxr-distortion-plus-mods-1

        Returns:
            Filter object
    """
    graph = Graph()

    # Knobs
    gain_param = 0.5
    mix_param = 0.5

    # Input / output
    node_in = Node(graph, fixed=True)
    node_out = Node(graph, fixed=True, output=True)

    # Supply
    node_4_5 = Node(graph, value=4.5, fixed=True)
    node_gnd = Node(graph, value=0, fixed=True)

    # Op amp plus section
    edge = Edge(graph, node_in, node_gnd)
    capacitor = Capacitor(graph, .001 * Units.u, node_in, node_gnd, edge)
    graph.add_component(capacitor)

    node = Node(graph)
    edge = Edge(graph, node_in, node)
    capacitor = Capacitor(graph, .01 * Units.u, node_in, node, edge)
    graph.add_component(capacitor)

    node_plus = Node(graph)
    edge = Edge(graph, node, node_plus)
    resistor = Resistor(graph, 10 * Units.K, node, node_plus, edge)
    graph.add_component(resistor)

    edge = Edge(graph, node_plus, node_4_5)
    resistor = Resistor(graph, 1 * Units.M, node_plus, node_4_5, edge)
    graph.add_component(resistor)

    # Op amp minus section
    node = Node(graph)
    edge = Edge(graph, node, node_gnd)
    resistor = Resistor(graph, gain_param * (1 * Units.M), node, node_gnd, edge)
    graph.add_component(resistor)

    node_1 = Node(graph)
    edge = Edge(graph, node, node_1)
    resistor = Resistor(graph, 4.7 * Units.K, node, node_1, edge)
    graph.add_component(resistor)

    node_minus = Node(graph)
    edge = Edge(graph, node_1, node_minus)
    capacitor = Capacitor(graph, 0.047 * Units.u, node_1, node_minus, edge)
    graph.add_component(capacitor)

    # Op amp
    node_output = Node(graph)
    op_amp = Opamp(graph, node_a=node_minus, node_b=node_plus, node_out=node_output)
    graph.add_component(op_amp)

    edge = Edge(graph, node_minus, node_output)
    resistor = Resistor(graph, 1 * Units.M, node_minus, node_output, edge)
    graph.add_component(resistor)

    # Op amp output
    node = Node(graph)
    edge = Edge(graph, node_output, node)
    capacitor = Capacitor(graph, 1 * Units.u, node_output, node, edge)
    graph.add_component(capacitor)

    node_1 = Node(graph)
    edge = Edge(graph, node, node_1)
    resistor = Resistor(graph, 10 * Units.K, node, node_1, edge)
    graph.add_component(resistor)

    edge = Edge(graph, node_1, node_gnd)
    diode1 = Diode(graph, node_a=node_1, node_b=node_gnd, edge_i=edge)
    graph.add_component(diode1)

    edge = Edge(graph, node_gnd, node_1)
    diode2 = Diode(graph, node_a=node_gnd, node_b=node_1, edge_i=edge)
    graph.add_component(diode2)

    edge = Edge(graph, node_1, node_gnd)
    capacitor = Capacitor(graph, .001 * Units.u, node_1, node_gnd, edge)
    graph.add_component(capacitor)

    # Output potentiometer
    edge = Edge(graph, node_1, node_out)
    resistor = Resistor(graph, mix_param * (10 * Units.K), node_1, node_out, edge)
    graph.add_component(resistor)

    edge = Edge(graph, node_out, node_gnd)
    resistor = Resistor(graph, (1 - mix_param) * (10 * Units.K), node_out, node_gnd, edge)
    graph.add_component(resistor)

    mxr_filter = Filter(graph, node_in, node_out)
    return mxr_filter
