
from math import exp

import numpy as np
import matplotlib.pyplot as plt

from common_filters import LowPassFilter, NoninvertingOpAmpFilter
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
    #filename = "samples/clean_guitar.wav"
    filename = "samples/stratocaster.wav"

    mxr_filter = make_mxr_distortion_filter()
    input_signal = SH.load(filename, sampleperiod=Config.time_step, peak=1)
    output_signal = mxr_filter.execute(input_signal)
    #amp_filter = NoninvertingOpAmpFilter.make(100, 100)
    #input_signal = Signal.sine(1, 440, 1, 0)
    #output_signal = amp_filter.execute(input_signal)
    mxr_filter.plot_probes()

    #output_signal = amp_filter.execute(input_signal)
    print("Playing input...")
    SH.play(input_signal, bytespersample=2, peak=1)
    print("Playing output...")
    SH.play(output_signal, bytespersample=2, peak=1)
    SH.save(output_signal, "stratocasterout.wav", bytespersample=2, peak=1)
