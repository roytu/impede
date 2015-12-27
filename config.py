
""" Class object that stores settings about the program. """

class Config(object):
    epsilon = 0.00001
    """ Error threshold for equality """

    max_voltage = 100
    """ Maximum voltage we expect to use. """

    min_voltage = -100
    """ Minimum voltage we expect to use. """

    max_current = 1
    """ Maximum current we expect to use. """

    min_current = -1
    """ Minimum current we expect to use. """

    resolution_step = 0.1
    """ Factor to decrease step until things work """
