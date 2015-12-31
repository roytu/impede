
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
        i = 0
        start = clock()
        for input_voltage in voltages:
            self._input_node.set_value(input_voltage)
            self._graph.solve()
            output_voltage = self._output_node.value()
            output_voltages.append(output_voltage)
            print("{0} / {1}".format(i, len(voltages)))
            i += 1
        diff = clock() - start
        print("Time elapsed (s): {0}".format(diff))
        return output_voltages
