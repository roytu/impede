
""" Module containing classes to generate common filters. """

from math import pi

from graph import Node, Graph
from resistor import Resistor
from capacitor import Capacitor
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

        input_node = Node(graph, fixed=True)
        output_node = Node(graph)
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
