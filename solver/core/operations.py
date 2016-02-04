from .numbers import Number
from .symbol import Symbol
from .expr import Expression

from operator import mul

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


class Mul(Expression):

    symbol = '*'
    precedence = 3
    association = 'left'
    commutative = True

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

    """def __new__(cls, *args):
        obj = Expression.__new__(cls, *args)

        # If all args are numbers just evaluate
        if all(isinstance(arg, Number) for arg in args):
            return sum(args, Number(0))

        # If there's only one arg return that
        if len(obj.args) == 1:
            return obj.args[0]

        return obj"""
