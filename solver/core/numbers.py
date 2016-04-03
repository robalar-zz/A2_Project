from .base import Atom
from fractions import Fraction


class Number(Atom):

    def __new__(cls, *args):

        if cls is Number:
            if len(args) == 1:
                arg = args[0]

                if isinstance(arg, (int, long)):
                    return super(Number, cls).__new__(Integer, arg)
                elif isinstance(arg, (basestring, float, Fraction)):
                    return super(Number, cls).__new__(Rational, arg)

            if len(args) == 2:
                return super(Number, cls).__new__(Rational, *args)

        else:
            return super(Number, cls).__new__(cls, *args)

    def __mul__(self, other):

        if isinstance(other, Number):
            return Number(self.value * other.value)

        return super(Number, self).__mul__(other)

    def __pow__(self, power, modulo=None):

        from .operations import denominator

        if isinstance(power, Integer):
            return Number(self.value ** power.value)
        elif isinstance(power, Rational) and is_nth_root(self, denominator(power)):
            v = self.value ** power.value
            return Number(v)

        return super(Number, self).__pow__(power)

    def __add__(self, other):

        if isinstance(other, Number):
            return Number(self.value + other.value)

        return super(Number, self).__add__(other)

    def __iadd__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

        return super(Number, self).__add__(other)

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        else:
            return super(Number, self).__eq__(other)

    def __ne__(self, other):
        return ~self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Number):
            return self.value < other.value
        else:
            return False

    def __abs__(self):
        return Number(abs(self.value))

    def __repr__(self):
        return str(self.value)

class Undefined(object):
    """ For calculations where the result is not known i.e. 0/0, 0^0, oo/oo
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


class Infinity(Undefined):

    def __gt__(self, other):
        return True

    def __lt__(self, other):
        return False

    def __repr__(self):
        return 'oo'


class Integer(Number):

    def __init__(self, value):
        super(Integer, self).__init__()
        self.value = value


class Rational(Number):
    """ Purely a wrapper for the builtin fraction class
    """
    
    def __init__(self, *args):

        self.value = Fraction(*args).limit_denominator()
        super(Rational, self).__init__()

        self.numerator = self.value.numerator
        self.denominator = self.value.denominator

    def __str__(self):
        return self.value.__str__()


def is_nth_root(value, root):

    if not isinstance(value, Number) or not isinstance(root, Number):
        raise ValueError('value and root must both be Numbers not {} and {}'.format(type(value), type(root)))

    u = value.value ** (1.0/root.value)
    u = long(round(u))
    return u ** root.value == value.value
