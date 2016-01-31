
""" Common module to inherit for tests. """

def test(expected, actual, epsilon=0):
    """ Takes expected and actual values.  If they are different by
    more than epsilon, then print a fail string.  Otherwise, print a pass string.

    >>> test(2, 2)
    PASS: Got 2
    >>> test(2, 2.001, epsilon=.01)
    PASS: Got 2.001
    >>> test(2, 3)
    FAIL: Expected 2, got 3
    """
    if abs(expected - actual) <= epsilon:
        print("PASS: Got {0}".format(actual))
    else:
        print("FAIL: Expected {0}, got {1}".format(expected, actual))
