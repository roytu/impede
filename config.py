
""" Class object that stores settings about the program. """

from units import Units

class Config(object):
    epsilon = 0.001
    """ Error threshold for equality """

    time_step = float(1) / 44100
    """ Number of seconds per timestep """
