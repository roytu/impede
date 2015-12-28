
""" Class object that stores settings about the program. """

from units import Units

class Config(object):
    epsilon = 0.001
    """ Error threshold for equality """

    max_voltage = 20
    """ Maximum voltage we expect to use. """

    min_voltage = -20
    """ Minimum voltage we expect to use. """

    max_current = 0.1
    """ Maximum current we expect to use. """

    min_current = -0.1
    """ Minimum current we expect to use. """

    resolution_step = 0.1
    """ Factor to decrease step until things work """

    time_step = 100 * Units.u
    """ Number of seconds per timestep """
