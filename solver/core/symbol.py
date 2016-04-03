from .base import Atom
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
    
    def __add__(self, other):
        return super(Symbol, self).__add__(other)
    
    def __mul__(self, other):
        return super(Symbol, self).__mul__(other)
        
    def __pow__(self, power, modulo=None):
        super(Symbol, self).__pow__(power)

    def __eq__(self, other):

        if isinstance(other, Symbol):
            return self.name == other.name
        else:
            super(Symbol, self).__eq__(other)

    def __ne__(self, other):
        if isinstance(other, Symbol):
            return self.name != other.name
        else:
            super(Symbol, self).__ne__(other)
    
    def __lt__(self, other):
        return super(Symbol, self).__lt__(other)
    
    def __repr__(self):
        return self.name
    
    def __or__(self, other):
        return super(Symbol, self).__or__(other)

class ReservedSymbol(Symbol, Number):
    """ Used to represent numbers like pi and e that have values but are imprecise.

        Attributes:
            name: name of the symbol
            value: approximate value of the symbol
    """
    def __init__(self, name, value):
        super(ReservedSymbol, self).__init__(name)
        self.value = value

    def __eq__(self, other):
        if isinstance(other, ReservedSymbol):
            return self.name == other.name
        else:
            super(ReservedSymbol, self).__eq__(other)
            
    def __lt__(self, other):
        if isinstance(other, ReservedSymbol):
            return self.name < other.name
        else:
            return super(ReservedSymbol, self).__lt__(other)