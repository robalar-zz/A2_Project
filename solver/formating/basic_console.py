from ..core.operations import Add, Mul, Pow
from ..core.symbol import Symbol
from ..core.numbers import Number, Rational
from ..core.function import Function


def basic_console(u, prior_presedence=0):
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
            result = '(' + result + ')'

        return result

    if isinstance(u, Function):
        return u.name + '(' + str(u.args)[1:-1] + ')'

    else:
        return u


def format_operator(u):
    l = [basic_console(x, u.precedence) for x in joinit(u.args, u.symbol)]
    return ''.join(l)


def joinit(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x