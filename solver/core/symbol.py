from .base import Atom


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
        return super(Symbol, self).__pow__(power)

    def __eq__(self, other):

        if isinstance(other, Symbol):
            return self.name == other.name
        else:
            return super(Symbol, self).__eq__(other)
    
    def __lt__(self, other):
        return super(Symbol, self).__lt__(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class Undefined(Symbol):
    
    def __init__(self):
        super(Undefined, self).__init__('Undefined')
    
    def __add__(self, other):
        return self

    def __mul__(self, other):
        return self

    def __pow__(self, power, modulo=None):
        return self

    def __lt__(self, other):
        return self

    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True