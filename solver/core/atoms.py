class Base(object):
    """ Base class for all other objects, this is so all types can be manipulated generally.
    """

    def __new__(cls):
        obj = object.__new__(cls)
        return obj

    def __add__(self, other):
        from .operations import Add
        return Add(self, other)

    def __pos__(self):
        return self

    def __neg__(self):
        return -1 * self

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
        from .operations import Mul, Pow
        return Mul(self, Pow(other, -1))

    def __sub__(self, other):
        from .operations import Add, Mul
        return Add(self, Mul(-1, other))

    def __rsub__(self, other):
        return self.__sub__(other)

    def __repr__(self):
        return '{}'.format(self.__class__.__name__)

    def __deepcopy__(self, memo):
        return self

class Atom(Base):
    """ Base class for any atomic type.
    """

    def __new__(cls):
        obj = Base.__new__(cls)
        obj.args = tuple()  # Must have no sub-expressions

        return obj

