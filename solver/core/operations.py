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


class Mul(Expression):

    symbol = '*'
    precedence = 3
    association = 'left'
    commutative = True


class Add(Expression):

    symbol = '+'
    precedence = 2
    association = 'left'
    commutative = True
    callback = sum


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


def term(u):
    # Assumes that the constant (number) is the first arg, as it should be with the correct ordering,
    # and there is only one constant

    if isinstance(u, (Symbol, Add, Pow)):
        return Mul(u)
    if isinstance(u, Mul) and isinstance(u.args[0], Number):
        return Mul(*u.args[1:])
    if isinstance(u, Mul) and not isinstance(u.args[0], Number):
        return u
    if isinstance(u, Number):
        return Undefined


def const(u):
    if isinstance(u, (Symbol, Add, Pow)):
        return Number(1)
    if isinstance(u, Mul) and isinstance(u.args[0], Number):
        return u.args[0]
    if isinstance(u, Mul) and not isinstance(u.args[0], Number):
        return Number(1)
    if isinstance(u, Number):
        return Undefined

