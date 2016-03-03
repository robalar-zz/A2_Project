from .numbers import Number, Undefined, Rational
from .symbol import Symbol
from .expr import Expression
from .function import Function


class Eq(Expression):

    symbol = '='

    def __new__(cls, *args):
        raise NotImplementedError


class Pow(Expression):

    symbol = '^'
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


def base(u):
    if isinstance(u, (Symbol, Mul, Add, Function)):
        return u
    if isinstance(u, Pow):
        return u.base
    if isinstance(u, Number):
        return Undefined()


def exponent(u):
    if isinstance(u, (Symbol, Mul, Add, Function)):
        return Number(1)
    if isinstance(u, Pow):
        return u.exponent
    if isinstance(u, Number):
        return Undefined()


def term(u):
    # Assumes that the constant (number) is the first arg, as it should be with the correct ordering,
    # and there is only one constant

    if isinstance(u, (Symbol, Add, Pow, Function)):
        return Mul(u)
    if isinstance(u, Mul) and isinstance(u.args[0], Number):
        return Mul(*u.args[1:])
    if isinstance(u, Mul) and not isinstance(u.args[0], Number):
        return u
    if isinstance(u, Number):
        return Undefined()


def const(u):
    if isinstance(u, (Symbol, Add, Pow, Function)):
        return Number(1)
    if isinstance(u, Mul) and isinstance(u.args[0], Number):
        return u.args[0]
    if isinstance(u, Mul) and not isinstance(u.args[0], Number):
        return Number(1)
    if isinstance(u, Number):
        return Undefined()


def numerator(u):
    if isinstance(u, Rational):
        return Number(u.numerator)  # FIXME: Number conversion should be handled in Rational
    elif isinstance(u, Pow):
        if exponent(u) < Number(0):
            return Number(1)
        else:
            return u
    elif isinstance(u, Mul):
        v = u.args[0]
        return numerator(v) * numerator(u/v)
    else:
        return u


def denominator(u):
    if isinstance(u, Rational):
        return Number(u.denominator)
    elif isinstance(u, Pow):
        if exponent(u) < Number(0):
            return base(u) ** abs(exponent(u))
        else:
            return Number(1)
    elif isinstance(u, Mul):
        v = u.args[0]
        return denominator(v) * denominator(u/v)
    else:
        return Number(1)


def rationalise_sum(u, v):
    """
        m/r + n/s => (ms + nr)/(rs)
    """

    m = numerator(u)
    r = denominator(u)
    n = numerator(v)
    s = denominator(v)

    if r == Number(1) and s == Number(1):
        return u + v
    else:
        return rationalise_sum(m * s, n * r)/(r * s)


def rationalise(u):
    if isinstance(u, Pow):
        return rationalise(u.base) ** u.exponent
    elif isinstance(u, Mul):
        f = u.args[0]
        return rationalise(f) * rationalise(u/f)
    elif isinstance(u, Add):
        f = u.args[0]
        g = rationalise(f)
        r = rationalise(u - f)
        return rationalise_sum(g, r)
    else:
        return u


def rational_expand(u):
    from ..polynomials.general_polynomial import expand
    v = rationalise(u)
    return rationalise(expand(numerator(v)) * expand(denominator(v)))

def rational_variables(u):
    from ..polynomials.general_polynomial import variables
    return variables(denominator(u)) | variables(numerator(u))