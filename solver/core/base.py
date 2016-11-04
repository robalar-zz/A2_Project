from abc import abstractmethod, ABCMeta


class Base(object):
    """ Base class for all other objects, this is so all types can be manipulated generally.

    This class is an abstract base class (direct instances of it can never be created), and defined certain methods that
    must be overridden by its children, at the very least with a call to super(...) to enable default behaviour.

    To write an object that derives from Base the following methods *must* be implemented;
    - __mul__
    - __pow__
    - __add__
    - __eq__
    - __lt__

    These methods should return a known interaction (ie Number + Number -> Number) or a call to super(...), which will
    eventually create the appropriate operator instance. Of course other methods can be overridden but this should not be
    necessary for most use cases.

    """

    __metaclass__ = ABCMeta

    #Arithmetic magic methods

    @abstractmethod
    def __mul__(self, other):
        from .operations import Mul
        return Mul(self, other)

    def __rmul__(self, other):
        return self * other

    @abstractmethod
    def __pow__(self, power, modulo=None):
        from .operations import Pow
        return Pow(self, power)

    def __rpow__(self, power, modulo=None):
        return self ** power

    @abstractmethod
    def __add__(self, other):
        from .operations import Add
        return Add(self, other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + -1 * other

    def __rsub__(self, other):
        return other + -1 * self

    def __div__(self, other):
        return self * other**-1

    def __rdiv__(self, other):
        return other * self**-1

    def __neg__(self):
        return -1 * self

    # Equality magic methods

    @abstractmethod
    def __eq__(self, other):  # DO NOT TRY AND IMPLEMENT EQUATIONS HERE!!!!
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @abstractmethod
    def __lt__(self, other):
        from .operations import LessThan
        return LessThan(self, other)

    def __gt__(self, other):
        return not self < other and self != other

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)

    # Boolean magic methods

    def __and__(self, other):
        from .operations import And
        return And(self, other)

    def __or__(self, other):
        from .operations import Or
        return Or(self, other)

    def __invert__(self):
        from .operations import Not
        return Not(self)

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError('A class derivied from base must implement its own hash method')

    #Printing methods
    @property
    def basic_string(self):
        raise NotImplementedError('No basic string representation implemented in {}'.format(self.__class__))

    def __str__(self):
        return self.basic_string


class FlyweightMixin(object):
    _instances = dict()

    def __new__(cls, *args, **kargs):
        return cls._instances.setdefault(
                    (cls, args, tuple(kargs.items())),
                    object.__new__(cls))


class Atom(Base, FlyweightMixin):
    """ Base class for any atomic type.
    """

    __metaclass__ = ABCMeta

    pass