
""" Extra functions module. """

def irangef(start, stop, step=1):
    """ Inclusive range with floating point step.  Returns a list.

    Args:
        start : First element
        stop : Last element
        step : Amount to increment by each time
    Returns:
        list

    >>> irangef(0, 5, 1)
    [0, 1, 2, 3, 4, 5]
    """
    result = []

    i = start
    while i <= stop:
        result.append(i)
        i += step
    return result
