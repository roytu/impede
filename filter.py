
""" Filter module """

from time import clock

class Filter(object):
    """ A Filter object takes a circuit and supports functionality that
    takes in a voltage-time signal and returns a new voltage-time signal.
    """
    def __init__(self, graph, input_node, output_node):
        self._graph = graph
        self._input_node = input_node
        self._output_node = output_node

    def execute(self, voltages):
        """ Given a list of voltages, return a new list of voltages
        corresponding to those put through the signal.

        Args:
            signal : List of voltages (float)

        Return:
            list of voltages (float)
        """
        output_voltages = []
        for i, input_voltage in enumerate(voltages):
            self._input_node.set_value(input_voltage)
            self._graph.solve()
            output_voltage = self._output_node.value()
            output_voltages.append(output_voltage)

            if i % 100 == 0:
                print("{0} / {1}".format(i, len(voltages)))
        print(output_voltages)
        return output_voltages
