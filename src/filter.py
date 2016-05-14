
""" Filter module """

import numpy as np
import matplotlib.pyplot as plt

from time import clock

class Filter(object):
    """ A Filter object takes a circuit and supports functionality that
    takes in a voltage-time signal and returns a new voltage-time signal.
    This function also takes a list of nodes to be used as probe points,
    and a function exists to plot the history of the nodes.

    Args:
        input_node : Node object
        output_node : Node object
        probes : list of Node objects (or None)

    Returns:
        Filter object
    """
    def __init__(self, graph, input_node, output_node, probes=None):
        self._graph = graph
        self._input_node = input_node
        self._output_node = output_node
        if not probes:
            probes = []
        self._probes = probes
        self._probe_values = dict()

    def execute(self, voltages):
        """ Given a list of voltages, return a new list of voltages
        corresponding to those put through the signal.

        Args:
            signal : List of voltages (float)

        Return:
            list of voltages (float)
        """
        output_voltages = []

        input_voltage_var = Symbol("v_i")
        self._input_node.set_value(input_voltage_var)

        # output_voltage = self._output_node.value()  # this should be here ish
        func = self._graph.solve()

        # TODO add probes back in
        #for probe in self._probes:
        #    if probe not in self._probe_values:
        #        self._probe_values[probe] = []
        #    self._probe_values[probe].append(probe.value())
        for i, input_voltage in enumerate(voltages):
            # TODO perform substitution and evaluate
            output_voltage = func(input_voltage)
            output_voltages.append(output_voltage)

            if i % 100 == 0:
                print("{0} / {1}".format(i, len(voltages)))
        print(output_voltages)
        return output_voltages

    def plot_probes(self):
        """ Plots the time history of all probes.  Call only after running
        execute. """
        plt.title("Probe Plot")
        plt.xlabel("Sample")
        plt.ylabel("Voltage")
        for probe in self._probes:
            values = self._probe_values[probe]
            plt.plot(values, label=str(probe))
        plt.legend()
        plt.show()
