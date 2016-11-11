from .base import Atom
from .expr import Expression


class Symbol(Atom):
    """ Represents an algebraic constant.

    An atomic algebraic component that can be used in expressions alongside numbers and other symbols.

    Attributes:
        name: A string identifier that is unique
    """

    def __init__(self, name):
        
        super(Symbol, self).__init__()
        
        if not isinstance(name, (str, unicode)):
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

    @property
    def basic_string(self):
        return str(self.name)

    def __repr__(self):
        return self.name


class Undefined(Symbol):
    
    def __init__(self, name='Undefined'):
        super(Undefined, self).__init__(name)
    
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


class Infinity(Undefined):

    def __init__(self):
        super(Infinity, self).__init__('Infinity')

    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return False


class NegativeInfinity(Undefined):

    def __init__(self):
        super(NegativeInfinity, self).__init__('-Infinity')

    def __lt__(self, other):
        return False

    def __gt__(self, other):
        return True

def free_symbols(u):

    if isinstance(u, Expression):
        return set().union(*[free_symbols(x) for x in u.args])
    elif isinstance(u, Symbol):
        return {u}
    else:
        return set()