from .atoms import Atom
from .numbers import Number


class Symbol(Atom):
    """ Represents an algebraic constant.

    An atomic algebraic component that can be used in expressions alongside numbers and other symbols.

    Attributes:
        name: A string identifier that is unique
    """

    def __init__(self, name):
        
        super(Symbol, self).__init__()
        
        if not isinstance(name, str):
            raise TypeError('A symbols name must be a string not {}'.format(type(name)))
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):

        if isinstance(other, Symbol):
            return self.name == other.name
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class ReservedSymbol(Symbol):
    """ Used to represent numbers like pi and e that have values but are imprecise.

        Attributes:
            name: name of the symbol
            value: approximate value of the symbol
    """
    def __init__(self, name, value):
        super(ReservedSymbol, self).__init__(name)

        if not isinstance(value, Number):
            raise ValueError('A reserved symbol must have a Number value')

        self.value = value

    def __eq__(self, other):
        if isinstance(other, ReservedSymbol):
            return self.name == other.name
        if isinstance(other, Number):
            return self.value == other

    def __lt__(self, other):
        if isinstance(other, Number):
            return self.value < other

    def __le__(self, other):
        if isinstance(other, Number):
            return self.value <= other

    def __gt__(self, other):
        if isinstance(other, Number):
            return self.value > other

    def __ge__(self, other):
        if isinstance(other, Number):
            return self.value >= other
