class Atom(object):
    """ Base class for any atomic type
    """

    def __add__(self, other):
        from .operations import Add
        return Add(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        from .operations import Mul
        return Mul(self, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power, modulo=None):
        from .operations import Pow
        return Pow(self, power)

    def __div__(self, other):
        from .operations import Div
        return Div(self, other)


class Number(Atom):
    pass


class Integer(Number):

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value + other.value)

    def __iadd__(self, other):
        return self + other

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):

        if isinstance(other, Integer):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
