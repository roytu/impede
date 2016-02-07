
""" Module that contains some example filters """

import numpy as np
import matplotlib.pyplot as plt

from graph import Node, Edge, Graph
from components.resistor import Resistor
from components.capacitor import Capacitor
from components.diode import Diode
from components.opamp import Opamp
from components.wire import Wire
from units import Units
from filter import Filter

def make_mxr_distortion_filter():
    """ Return the MXR filter from:

        http://www.premierguitar.com/articles/mxr-distortion-plus-mods-1

        Returns:
            Filter object
    """
    probes = []

    graph = Graph()

    # Knobs
    gain_param = 0.5
    mix_param = 0.1

    # Input / output
    node_in = Node(graph, fixed=True, source=True, label="Vin")
    node_out = Node(graph, output=True, label="Vout")

    # Supply
    node_4_5 = Node(graph, value=4.5, fixed=True, source=True, label="4.5V")
    node_gnd = Node(graph, value=0, fixed=True, source=True, label="GND")

    # Probe Vin
    probes.append(node_in)

    # Op amp plus section
    edge = Edge(graph, node_in, node_gnd, label="I1")
    capacitor = Capacitor(graph, .001 * Units.u, node_in, node_gnd, edge)
    graph.add_component(capacitor)

    node = Node(graph, label="V1")
    edge = Edge(graph, node_in, node, label="I2")
    #capacitor = Capacitor(graph, .01 * Units.u, node_in, node, edge)
    #graph.add_component(capacitor)
    wire = Wire(graph, node_in, node, edge)
    graph.add_component(wire)

    node_plus = Node(graph, label="V+")
    edge = Edge(graph, node, node_plus, label="I3")
    resistor = Resistor(graph, 10 * Units.K, node, node_plus, edge)
    graph.add_component(resistor)

    edge = Edge(graph, node_plus, node_4_5, label="I4")
    resistor = Resistor(graph, 1 * Units.M, node_plus, node_4_5, edge)
    graph.add_component(resistor)

    # Op amp minus section
    node = Node(graph, label="V2")
    edge = Edge(graph, node, node_gnd, label="I5")
    resistor = Resistor(graph, gain_param * (1 * Units.M), node, node_gnd, edge)
    graph.add_component(resistor)

    node_1 = Node(graph, label="V3")
    edge = Edge(graph, node, node_1, label="I6")
    resistor = Resistor(graph, 4.7 * Units.K, node, node_1, edge)
    graph.add_component(resistor)

    node_minus = Node(graph, label="V-")

    edge = Edge(graph, node_1, node_minus, label="I7")
    #capacitor = Capacitor(graph, 0.047 * Units.u, node_1, node_minus, edge)
    #graph.add_component(capacitor)
    wire = Wire(graph, node_1, node_minus, edge)
    graph.add_component(wire)

    # Op amp
    node_output = Node(graph, source=True, label="Vo")
    op_amp = Opamp(graph, node_a=node_minus, node_b=node_plus, node_out=node_output)
    graph.add_component(op_amp)

    edge = Edge(graph, node_minus, node_output, label="I8")
    resistor = Resistor(graph, 1 * Units.M, node_minus, node_output, edge)
    graph.add_component(resistor)

    # Op amp output
    node = Node(graph, label="V4")
    edge = Edge(graph, node_output, node, label="I9")
    capacitor = Capacitor(graph, 1 * Units.u, node_output, node, edge)
    graph.add_component(capacitor)

    node_1 = Node(graph, label="V5")
    edge = Edge(graph, node, node_1, label="I10")
    resistor = Resistor(graph, 10 * Units.K, node, node_1, edge)
    graph.add_component(resistor)

    edge = Edge(graph, node_1, node_gnd, label="I11")
    diode1 = Diode(graph, node_a=node_1, node_b=node_gnd, edge_i=edge)
    graph.add_component(diode1)

    edge = Edge(graph, node_gnd, node_1, label="I12")
    diode2 = Diode(graph, node_a=node_gnd, node_b=node_1, edge_i=edge)
    graph.add_component(diode2)

    edge = Edge(graph, node_1, node_gnd, label="I13")
    capacitor = Capacitor(graph, .001 * Units.u, node_1, node_gnd, edge)
    graph.add_component(capacitor)

    # Output potentiometer
    edge = Edge(graph, node_1, node_out, label="I14")
    resistor = Resistor(graph, mix_param * (10 * Units.K), node_1, node_out, edge)
    graph.add_component(resistor)

    edge = Edge(graph, node_out, node_gnd, label="I15")
    resistor = Resistor(graph, (1 - mix_param) * (10 * Units.K), node_out, node_gnd, edge)
    graph.add_component(resistor)

    # Probe Vout
    probes.append(node_out)

    mxr_filter = Filter(graph, node_in, node_out, probes=probes)
    return mxr_filter
