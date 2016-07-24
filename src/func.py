
""" A Func is a callable that takes a sympy expression and returns
    a function that takes a dictionary of substitutions and
    returns a float.
"""

import sympy as sy
from tests import test

class Func(object):
    def __init__(self, expr):
        self.free_symbols = list(expr.free_symbols)
        self.fast_func = sy.lambdify(self.free_symbols, expr)

    def __call__(self, subs):
        """ Evaluates the function.  This should be FAST!

            Args:
                subs: dict of (var, value) items

            Returns:
                float
        """
        values = [subs[s] for s in self.free_symbols]
        return self.fast_func(*values)

if __name__ == "__main__":
    x, y = sy.symbols("x y")

    res = Func(x)({x: 3})
    test(3, res)

    res = Func(x * y)({x: 3, y: 2})
    test(6, res)
