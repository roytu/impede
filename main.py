
from __future__ import print_function

from math import exp

import numpy as np
import matplotlib.pyplot as plt

from common_filters import LowPassFilter
from signals import Signal
from units import Units
from sound_handler import SoundHandler as SH
from graph import Node, Edge, Graph
from diode import Diode
from tests import test
from config import Config
from util import irangef
from opamp import Opamp
from filter_library import make_mxr_distortion_filter

if __name__ == "__main__":
    """
    r = 318
    c = 1 * Units.u
    lpf = LowPassFilter.make(r, c)
    print("Cutoff frequency: {0}".format(LowPassFilter.cutoff_frequency(r, c)))

    input_signal = Signal.sine(1, 1000, 5)
    output_signal = lpf.execute(input_signal)
    SH.play(input_signal, bytespersample=1, peak=5)
    SH.play(output_signal, bytespersample=1, peak=5)
    """
    """
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

    plt.plot(voltages, currents)
    plt.show()
    """
    """
    graph = Graph()
    node_out = Node(graph, output=True)
    node_in = Node(graph, value=5, fixed=True)
    op_amp = Opamp(graph, node_a=node_out, node_b=node_in, node_out=node_out)
    graph.add_component(op_amp)
    graph.solve()
    test(5, node_out.value(), epsilon=Config.epsilon)
    """

    filename = "samples/clean_guitar.wav"

    mxr_filter = make_mxr_distortion_filter()
    input_signal = SH.load(filename, peak=1)
    output_signal = mxr_filter.execute(input_signal)
    SH.play(input_signal, bytespersample=1, peak=1)
    SH.play(output_signal, bytespersample=1, peak=1)
