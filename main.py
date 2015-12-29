
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

from common_filters import LowPassFilter
from signals import Signal
from units import Units

if __name__ == "__main__":
    r = 318
    c = 1 * Units.u
    lpf = LowPassFilter.make(r, c)
    print("Cutoff frequency: {0}".format(LowPassFilter.cutoff_frequency(r, c)))

    fs, transfers = [], []
    for f in range(100, 1000, 100):
        input_signal = Signal.sine(0.1, f, 5)
        output_signal = lpf.execute(input_signal)

        fs.append(f)
        transfers.append(max(output_signal) / 5)

        #plt.plot(input_signal, label="Input: {0} Hz".format(f))
        #plt.plot(output_signal, label="Output: {0} Hz".format(f))

    plt.xlabel("Frequency (in Hz.)")
    plt.ylabel("Gain")
    plt.plot(fs, transfers)
    plt.legend()
    plt.show()
