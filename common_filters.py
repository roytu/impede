
""" Module containing classes to generate common filters. """

from math import pi

from graph import Node, Graph
from resistor import Resistor
from capacitor import Capacitor
from filter import Filter
from opamp import Opamp

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

        input_node = Node(graph, fixed=True)
        output_node = Node(graph, output=True)
        ground_node = Node(graph, fixed=True, value=0)

        # Add resistor from input to output
        graph.add_component(Resistor(graph, r, input_node, output_node))
        # Add capacitor from output to ground
        graph.add_component(Capacitor(graph, c, output_node, ground_node))

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

        input_node = Node(graph, fixed=True)
        output_node = Node(graph, output=True)
        ground_node = Node(graph, fixed=True, value=0)

        node_minus = Node(graph)

        # Add resistor from input to V-
        graph.add_component(Resistor(graph, r1, input_node, node_minus))
        # Add resistor from V- to output
        graph.add_component(Resistor(graph, r2, node_minus, output_node))
        # Make op amp
        graph.add_component(Opamp(graph, node_minus, ground_node, output_node))

        inverting_filter = Filter(graph, input_node, output_node)
        return inverting_filter

    @staticmethod
    def gain(r1, r2):
        """ Returns the gain. """
        return -float(r2) / r1
