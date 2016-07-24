
""" A Constraint takes the form:

    c_0 * x_0 + c_1 * c_1 + ... = b

    where cs are coefficients, xs are variables (Nodes or Edges) and b is
    a coefficient.
"""

class Constraint(object):
    def __init__(self, cs, xs, b=0):
        self.cs = cs
        self.xs = xs
        self.b = b
