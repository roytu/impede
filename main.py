
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

from common_filters import LowPassFilter
from signals import Signal
from units import Units

if __name__ == "__main__":
    r = 318
    c = 10 * Units.u
    lpf = LowPassFilter.make(r, c)

    input_signal = Signal.sine(0.01, 200, 5)
    output_signal = lpf.execute(input_signal)

    plt.plot(input_signal, label="Input")
    plt.plot(output_signal, label="Output")
    plt.legend()
    plt.show()
