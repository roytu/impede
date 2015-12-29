
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

from common_filters import LowPassFilter
from signals import Signal
from units import Units
from sound_handler import SoundHandler as SH

if __name__ == "__main__":
    r = 318
    c = 1 * Units.u
    lpf = LowPassFilter.make(r, c)
    print("Cutoff frequency: {0}".format(LowPassFilter.cutoff_frequency(r, c)))

    input_signal = Signal.sine(1, 1000, 5)
    output_signal = lpf.execute(input_signal)
    SH.play(input_signal, peak=5)
    SH.play(output_signal, peak=5)
