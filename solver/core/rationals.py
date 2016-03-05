from .symbol import Symbol
from .function import Function
from .numbers import Number, Integer
from .operations import denominator, numerator, Add, Pow, Mul
from ..polynomials.general_polynomial import coeff_var_monomial, mononomials, variables, expand, is_expanded
from .simplify import auto_simplify


def is_rationalized(u):

    if isinstance(u, (Number, Symbol, Function)):
        return True
    else:
        result = True
        s = rational_variables(u)

        for v in s:
            result = result and denominator(v) == Number(1) and rationalise(v) == v

        for v in mononomials(numerator(u)):
            coeff_part = coeff_var_monomial(v, s)[0]
            result = result and isinstance(coeff_part, Integer)

        for v in mononomials(denominator(u)):
            coeff_part = coeff_var_monomial(v, s)[0]
            result = result and isinstance(coeff_part, Integer)

        return result


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


# FIXME
def rational_expand(u):
    raise NotImplementedError


def rational_variables(u):
    return variables(denominator(u)) | variables(numerator(u))