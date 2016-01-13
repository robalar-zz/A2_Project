class Atom(object):
    """ Base class for any atomic type
    """

    def __pos__(self):
        return self

    def __neg__(self):
        return -1 * self

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

    def __repr__(self):
        try:
            return '{}({})'.format(self.__class__.__name__, self.args)
        except AttributeError:
            return '{}'.format(self.__class__.__name__)


class Undefined(Atom):
    pass

class Number(Atom):

    def __new__(cls, *args):

        if len(args) == 1:

            if isinstance(args[0], Number):
                return args[0]
            if isinstance(args[0], int):
                return super(Number, cls).__new__(Integer)


class Integer(Number):

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        else:
            Atom.__mul__(other)

    def __iadd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value * other.value)
        else:
            Atom.__mul__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power, modulo=None):

        if isinstance(power, Integer):
            if power.value == 0 and self.value == 0:
                return Undefined()

            return Integer(self.value ** power.value)
        else:
            Atom.__mul__(power)

    def __eq__(self, other):

        if isinstance(other, Integer):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
