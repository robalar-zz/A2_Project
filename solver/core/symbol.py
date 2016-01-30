from .atoms import Atom
from .expr import Expression

__author__ = 'Rob'


class Symbol(Atom):
    """ Represents an algebraic constant.

    An atomic algebraic component that can be used in expressions alongside numbers and other symbols.

    Attributes:
        name: A string identifier that is unique
    """

    __slots__ = ['name']

    def __new__(cls, name):
        obj = Atom.__new__(cls)

        if not isinstance(name, str):
            raise TypeError('A symbols name must be a string not {}'.format(type(name)))

        obj.name = name

        return obj

    def __repr__(self):
        return self.name

    def __eq__(self, other):

        if isinstance(other, Symbol):
            return self.name == other.name

        return False

    def __ne__(self, other):
        return not self.__eq__(other)
