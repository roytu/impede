
""" Scripts to run that plot crucial circuits """

import numpy as np
import matplotlib.pyplot as plt

from common_filters import LowPassFilter
from signals import Signal
from graph import Node, Edge, Graph
from components.diode import Diode
from components.resistor import Resistor
from components.capacitor import Capacitor
from config import Config
from units import Units
from util import irangef

def diode_iv_curve():
    """ Plots the IV curve of a diode. """
    plt.title("Diode IV Curve")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Current (A)")

    # Plot ideal
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

    plt.plot(voltages, currents, label="Voltage varies continuously")

    # Plot random
    SAMPLES = 1000

    currents = []
    voltages = np.random.random(SAMPLES) * 0.2 + 0.6
    graph = Graph()
    node_a = Node(graph, value=0, fixed=True)
    node_b = Node(graph, value=0, fixed=True)
    edge_i = Edge(graph, node_a, node_b)
    diode = Diode(graph, node_a, node_b, edge_i)
    graph.add_component(diode)

    for v in voltages:
        node_a.set_value(v)
        graph.solve()

        currents.append(edge_i.value())

    # Sort
    currents = (np.array(currents))[voltages.argsort()]
    voltages.sort()

    plt.plot(voltages, currents, label="Voltage varies randomly")
    plt.legend()
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

    cutoff_freq = LowPassFilter.cutoff_frequency(r, c)
    plt.title("Lowpass Transfer Curve (cutoff={0} Hz)".format(cutoff_freq))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Gain")
    plt.plot(fs, gains)
    plt.show()

def capacitor_charge_curve():
    """ Plots the charging of a capacitor overtime. """
    r = 100
    c = 10 * Units.u

    DURATION = 0.01

    ts = irangef(0, DURATION, Config.time_step)
    ts = np.array(ts)

    # Model
    graph = Graph()
    node_5 = Node(graph, value=5, fixed=True, source=True)
    node_gnd = Node(graph, value=0, fixed=True, source=True)
    node = Node(graph)

    # Resistor
    edge = Edge(graph, node_5, node)
    graph.add_component(Resistor(graph, r, node_5, node, edge))
    # Capacitor
    edge = Edge(graph, node, node_gnd)
    graph.add_component(Capacitor(graph, c, node, node_gnd, edge))

    vs = []
    for t in ts:
        graph.solve()

        v = node.value()

        np.append(ts, t)
        vs.append(v)

    plt.title("Capacitor Charge Curve (R = 100 Ohms, C = 10 uF, V = 5 V)")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.plot(ts, vs, label="Model")

    # Plot ideal
    vs_ideal = 5 * (1 - np.exp(-ts / (r * c)))
    plt.plot(ts, vs_ideal, label="Ideal")

    plt.legend()
    plt.show()

if __name__ == "__main__":
    #diode_iv_curve()
    #lowpass_filter_transfer_curve()
    capacitor_charge_curve()
