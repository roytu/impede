
""" Module that provides functions for signal generation """

from math import pi, sin

from config import Config
from util import irangef

class Signal(object):
    """ Static class to generate voltage signals.  Uses Config.time_step
    as the amount of time between samples. """
    @staticmethod
    def sine(length, frequency, amplitude, bias=0):
        """ Returns a sine wave given parameters.

        Args:
            length : float (in seconds)
            frequency : float (in Hz)
            amplitude : float (in volts)
            bias : float (in volts)

        Returns:
            list of voltages
        """
        voltages = []
        for t in irangef(0, length, step=Config.time_step):
            voltage = amplitude * sin((t * frequency) * 2 * pi) + bias
            voltages.append(voltage)
        return voltages
