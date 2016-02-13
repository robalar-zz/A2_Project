from .atoms import Atom


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


    def __repr__(self):
        return self.name

    def __eq__(self, other):

        if isinstance(other, Symbol):
            return self.name == other.name
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
