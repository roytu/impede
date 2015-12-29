
""" Class object that stores settings about the program. """

from units import Units

class Config(object):
    epsilon = 0.001
    """ Error threshold for equality """

    time_step = 100 * Units.u
    """ Number of seconds per timestep """
