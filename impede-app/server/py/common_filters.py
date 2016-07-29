
""" Module containing classes to generate common filters.

NOTE THAT ALL FILTERS ASSUME HIGH INPUT IMPEDANCE!!
"""

from math import pi

from graph import Node, Edge, Graph
from resistor import Resistor
from capacitor import Capacitor
from opamp import Opamp
from filter import Filter

class LowPassFilter(object):
    """ First order low pass filter """

    @staticmethod
    def make(r, c):
        """ Returns a low pass filter with resistance r and capacitance c.

        Args:
            r : resistance (float)
            c : capacitance (float)

        Returns:
            Filter object
        """
        graph = Graph()

        input_node = Node(graph, fixed=True, source=True)
        output_node = Node(graph, output=True)
        ground_node = Node(graph, value=0, fixed=True, source=True)

        # Add resistor from input to output
        edge = Edge(graph, input_node, output_node)
        resistor = Resistor(graph, r, input_node, output_node, edge)
        graph.add_component(resistor)

        # Add capacitor from output to ground
        edge = Edge(graph, output_node, ground_node)
        capacitor = Capacitor(graph, c, output_node, ground_node, edge)
        graph.add_component(capacitor)

        lowpass = Filter(graph, input_node, output_node)
        return lowpass

    @staticmethod
    def cutoff_frequency(r, c):
        """ Returns the cutoff frequency. """
        return 1 / (2 * pi * r * c)

class InvertingOpAmpFilter(object):
    """ Inverting op amp """

    @staticmethod
    def make(r1, r2):
        """ Returns an inverting op amp circuit with gain -R2 / R1

        Args:
            r1 : resistance from vin to v-
            r2 : resistance from v- to vout

        Returns:
            Filter object
        """
        graph = Graph()

        input_node = Node(graph, fixed=True, source=True, label="Vin")
        output_node = Node(graph, output=True, source=True, label="Vout")
        ground_node = Node(graph, value=0, fixed=True, source=True, label="GND")

        node_minus = Node(graph, label="V-")
        i1_edge = Edge(graph, input_node, node_minus, label="I1")
        i2_edge = Edge(graph, node_minus, output_node, label="I2")

        # Add resistor from input to V-
        graph.add_component(Resistor(graph, r1, input_node, node_minus, i1_edge))
        # Add resistor from V- to output
        graph.add_component(Resistor(graph, r2, node_minus, output_node, i2_edge))
        # Make op amp
        graph.add_component(Opamp(graph, node_minus, ground_node, output_node))

        inverting_filter = Filter(graph, input_node, output_node)
        return inverting_filter

    @staticmethod
    def gain(r1, r2):
        """ Returns the gain. """
        return -float(r2) / r1

class NoninvertingOpAmpFilter(object):
    """ Non-inverting op amp """

    @staticmethod
    def make(r1, r2):
        """ Returns a non-inverting op amp circuit with gain 1 + R2 / R1

        Args:
            r1 : resistance from v- to gnd
            r2 : resistance from v- to vout

        Returns:
            Filter object
        """
        probes = []

        graph = Graph()

        input_node = Node(graph, fixed=True, source=True, label="Vin")
        output_node = Node(graph, output=True, source=True, label="Vout")

        probes.append(input_node)
        probes.append(output_node)

        ground_node = Node(graph, value=0, fixed=True, source=True, label="GND")
        node_minus = Node(graph, label="V-")
        i1_edge = Edge(graph, node_minus, ground_node, label="I1")
        i2_edge = Edge(graph, node_minus, output_node, label="I2")

        # Add resistor from V- to GND
        graph.add_component(Resistor(graph, r1, node_minus, ground_node, i1_edge))
        # Add resistor from V- to output
        graph.add_component(Resistor(graph, r2, node_minus, output_node, i2_edge))
        # Make op amp
        graph.add_component(Opamp(graph, node_minus, input_node, output_node))

        noninverting_filter = Filter(graph, input_node, output_node, probes=probes)
        return noninverting_filter

    @staticmethod
    def gain(r1, r2):
        """ Returns the gain. """
        return 1 + float(r2) / r1
