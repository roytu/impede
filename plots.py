
""" Scripts to run that plot crucial circuits """

import matplotlib.pyplot as plt

from common_filters import LowPassFilter
from signals import Signal
from graph import Node, Edge, Graph
from diode import Diode
from units import Units
from util import irangef

def diode_iv_curve():
    """ Plots the IV curve of a diode. """
    voltages, currents = [], []
    for v in irangef(0.6, 0.8, 0.01):
        graph = Graph()
        node_a = Node(graph, value=v, fixed=True)
        node_b = Node(graph, value=0, fixed=True)
        edge_i = Edge(graph, node_a, node_b)
        diode = Diode(graph, node_a, node_b, edge_i)
        graph.add_component(diode)
        graph.solve()
        voltages.append(v)
        currents.append(edge_i.value())

    plt.title("Diode IV Curve")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")
    plt.plot(voltages, currents)
    plt.show()

def lowpass_filter_transfer_curve():
    """ Plots the transfer function of a lowpass filter with cutoff 500 Hz. """
    r = 318
    c = 1 * Units.u

    fs, gains = [], []
    for f in irangef(100, 1000, 50):
        lpf = LowPassFilter.make(r, c)
        input_signal = Signal.sine(0.01, f, 5)
        output_signal = lpf.execute(input_signal)

        gain = max(output_signal) / 5

        fs.append(f)
        gains.append(gain)

        #plt.plot(input_signal)
        #plt.plot(output_signal)
        #plt.show()

    cutoff_freq = LowPassFilter.cutoff_frequency(r, c)
    plt.title("Lowpass Transfer Curve (cutoff={0} Hz)".format(cutoff_freq))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Gain")
    plt.plot(fs, gains)
    plt.show()

if __name__ == "__main__":
    #diode_iv_curve()
    lowpass_filter_transfer_curve()
