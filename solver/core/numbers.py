from .atoms import Atom, Base

from fractions import Fraction

#TODO: Stop the __new__ inheritance? Create numbers in another way?

class Number(Atom):

    def __new__(cls, *args):

        if len(args) == 1:

            if isinstance(args[0], Number):
                return args[0]
            if isinstance(args[0], int):
                return super(Number, cls).__new__(Integer)
            if isinstance(args[0], basestring) or isinstance(args[0], Fraction):
                return super(Number, cls).__new__(Rational)

        if len(args) == 2:
            return super(Number, cls).__new__(Rational)


    def __repr__(self):
        return str(self.value)

    def __deepcopy__(self, memo):
        return self

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Number):
            return self.value < other.value
        else:
            return False

    def __le__(self, other):
        if isinstance(other, Number):
            return self.value <= other.value
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, Number):
            return self.value > other.value
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, Number):
            return self.value >= other.value
        else:
            return False

    def __abs__(self):
        return abs(Number(self.value))


class Undefined(object):
    """ For calculations where the result is known i.e. 0/0, 0^0, oo/oo
    """

    def __add__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __mul__(self, other):
        return self

    def __div__(self, other):
        return self

    def __repr__(self):
        return 'Undefined'


class Integer(Number):

    def __init__(self, value):
        
        super(Integer, self).__init__()
        
        self.value = value

class Rational(Number):
    """ Purely a wrapper for the builtin fraction class
    """
    
    def __init__(self, *args):
        super(Rational, self).__init__()
        
        self.value = Fraction(*args)
        self.numerator = self.value.numerator
        self.denominator = self.value.denominator

    def __str__(self):
        return self.value.__str__()


def sum(list):
    result = Number(0)
    for item in list:
        result += item

    return result