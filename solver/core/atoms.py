class Base(object):
    """ Base class for all other objects, this is so all types can be manipulated generally.
    """

    def __init__(self):
        pass

    def __add__(self, other):
        from .operations import Add
        return Add(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __pos__(self):
        return self

    def __neg__(self):
        return -1 * self

    def __mul__(self, other):
        from .operations import Mul
        return Mul(self, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power, modulo=None):
        from .operations import Pow
        return Pow(self, power)

    def __div__(self, other):
        from .operations import Mul, Pow
        return Mul(self, Pow(other, -1))

    def __sub__(self, other):
        from .operations import Add, Mul
        return Add(self, Mul(-1, other))

    def __rsub__(self, other):
        return self.__sub__(other)

    def __repr__(self):
        return '{}'.format(self.__class__.__name__)


class Atom(Base):
    """ Base class for any atomic type.
    """

    def __init__(self):
        super(Atom, self).__init__()
