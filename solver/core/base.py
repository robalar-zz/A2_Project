class Base(object):
    """ Base class for all other objects, this is so all types can be manipulated generally.
    """

    def __mul__(self, other):
        from .operations import Mul
        return Mul(self, other)

    def __rmul__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        from .operations import Pow
        return Pow(self, power)

    def __add__(self, other):
        from .operations import Add
        return Add(self, other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + -1 * other

    def __div__(self, other):
        return self * other**-1


class Atom(Base):
    """ Base class for any atomic type.
    """
    pass