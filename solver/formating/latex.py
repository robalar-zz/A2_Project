from ..core.operations import Add, Mul, Pow
from ..core.symbol import Symbol
from ..core.numbers import Number, Rational
from ..core.function import Function
from ..calculus.differentate import d
from ..core.matix import Matrix


def latex(u, prior_presedence=0):

    if isinstance(u, (Add, Mul, Pow)):
        result = format_operator(u)

        if u.precedence <= prior_presedence:
            result = '(' + result + ')'

        return result

    if isinstance(u, Symbol):
        return u.name

    if isinstance(u, Number):

        result = str(u.value)

        if isinstance(u, Rational):
            result = '\\frac{%d}{%d}' % (u.numerator, u.denominator)

        return result

    if isinstance(u, Function):
        return format_function(u)

    else:
        return u


def format_operator(u):
    if isinstance(u, Mul):
        l = [latex(x, u.precedence) for x in joinit(u.args, '')]
        l = ['-' if x == '-1' else x for x in l]
    elif isinstance(u, Add):
        l = [latex(x, u.precedence) for x in joinit(u.args, ' ' + u.symbol + ' ')]
    elif isinstance(u, Pow):
        l = [latex(u.base), '^{', latex(u.exponent), '}']

    s = ''.join(l)
    return s.replace('+ -', '- ')


def format_function(u):
    if isinstance(u, d):
        return u.name + '(' + str(u.args[0]) + ')'
    else:
        return u.name + '(' + str(u.args)[1:-1] + ')'


def joinit(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x
