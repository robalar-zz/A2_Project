from .numbers import Number, Undefined
from .symbol import Symbol
from .expr import Expression, subexpressions

from operator import mul, add

# TODO: Separate into functions?
# TODO: Separate into different files?


class Eq(Expression):

    symbol = '='

    def __new__(cls, *args):
        raise NotImplementedError


class Pow(Expression):

    symbol = '**'
    precedence = 4
    association = 'right'
    commutative = False
    
    def __init__(self, *args):

        if len(args) != 2:
            raise ValueError('Pow must have 2 args (base, exponent)')

        super(Pow, self).__init__(*args)

        self.base = args[0]
        self.exponent = args[1]

    
    """ def __new__(cls, *args):
        obj = Expression.__new__(cls, *args)

        if len(args) != 2:
            raise ValueError('Pow must have 2 args (base, exponent)')


        # If all the arguments are numbers just evaluate
        if all(isinstance(arg, Number) for arg in obj.args):
            return args[0] ** args[1]

        obj.base = args[0]
        obj.exponent = args[1]

        return obj"""


def product(iterable):
    result = Number(1)
    for i in iterable:
        result *= i
    return result

class Mul(Expression):

    symbol = '*'
    precedence = 3
    association = 'left'
    commutative = True

    def eval(self):
        print product([x for x in subexpressions(self, Number)])

    """def __new__(cls, *args):
        obj = Expression.__new__(cls, *args)

        # If all the arguments are numbers just evaluate
        if all(isinstance(arg, Number) for arg in args):
            return reduce(mul, args, Number(1))

        # If there's only one arg return that
        if len(obj.args) == 1:
            return obj.args[0]

        return obj"""

    def get_coefficient(self):
        return [i for i in self.args if isinstance(i, Number)][0]


class Add(Expression):

    symbol = '+'
    precedence = 2
    association = 'left'
    commutative = True
    callback = sum

    def eval(self):
        print sum([x for x in subexpressions(self, Number)])


    """def __new__(cls, *args):
        obj = Expression.__new__(cls, *args)

        # If all args are numbers just evaluate
        if all(isinstance(arg, Number) for arg in args):
            return sum(args, Number(0))

        # If there's only one arg return that
        if len(obj.args) == 1:
            return obj.args[0]

        return obj"""


def base(u):
    if isinstance(u, (Symbol, Mul, Add)):
        return u
    if isinstance(u, Pow):
        return u.base
    if isinstance(u, Number):
        return Undefined


def exponent(u):
    if isinstance(u, (Symbol, Mul, Add)):
        return Number(1)
    if isinstance(u, Pow):
        return u.exponent
    if isinstance(u, Number):
        return Undefined