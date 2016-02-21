from ..core.numbers import Integer, Number, Undefined, Rational
from ..core.operations import Pow, base, exponent, Mul, Add, numerator, denominator
from ..core.expr import free_of_set
from ..core.atoms import Atom

from math import factorial, floor


def is_mononomial_gpe(u, v):
    if not isinstance(v, set):
        variable_set = {v}
    else:
        variable_set = v

    if u in variable_set:
        return True

    elif isinstance(u, Pow):
        if base(u) in variable_set and isinstance(exponent(u), Integer) and exponent(u) > Number(1):
            return True
        else:
            return False

    elif isinstance(u, Mul):
        for operand in u.args:
            if not is_mononomial_gpe(operand, variable_set):
                return False
        return True

    return free_of_set(u, variable_set)


def is_polynomial_gpe(u, v):
    if not isinstance(v, set):
        variable_set = {v}
    else:
        variable_set = v

    if not isinstance(u, Add):
        return is_mononomial_gpe(u, set(variable_set))
    else:
        if u in variable_set:
            return True

        for operand in u.args:
            if not is_mononomial_gpe(operand, set(variable_set)):
                return False

        return True


def coeff_var_monomial(u, v):
    if not isinstance(v, set):
        variable_set = {v}
    else:
        variable_set = v

    if not is_mononomial_gpe(u, variable_set):
        return Undefined()
    else:
        if isinstance(u, Mul):
            coefficient_part = [c for c in u.args if free_of_set(c, variable_set)]
            variable_part = [v for v in u.args if v not in coefficient_part]
        else:
            variable_part = [u]
            coefficient_part = [Number(1)]

    return [coefficient_part, variable_part]


def collect_terms(u, variable_set):
    if not isinstance(u, Add):
        if isinstance(coeff_var_monomial(u, variable_set), Undefined):
            return Undefined()
        else:
            return u
    else:
        if u in variable_set:
            return u
        T = []
        for operand in u.args:
            f = coeff_var_monomial(operand, variable_set)
            if isinstance(f, Undefined):
                return Undefined()
            else:
                combined = False
                for i, other_operand in enumerate(T):
                    if f[1] == other_operand[1]:
                        T[i] = [Mul(*f[0]) + Mul(*other_operand[0]), f[1]]
                        combined = True
                        break
                if not combined:
                    T.append(f)

        v = Number(0)
        for item in T:
            v = v + Mul(item[0], *item[1])
        return v


def expand_product(r, s):

    if isinstance(r, Add):
        if isinstance(s, Atom):
            return expand(distribute(Mul(s, r)))

        f = r.args[0]
        return expand_product(f, s) + expand_product(r - f, s)
    elif isinstance(s, Add):
        return expand_product(s, r)
    else:
        return r * s


def expand_power(u, n):

    if not isinstance(n, Integer):
        raise ValueError('n must be and integer, not {}'.format(type(n)))

    if isinstance(u, Add):
        f = u.args[0]
        r = u - f
        s = Number(0)
        for k in range(n.value+1):
            c = Number(factorial(n.value)/(factorial(k) * factorial(n.value - k)))
            s = s + expand_product(c * f**Number(n.value-k), expand_power(r, Number(k)))
        return s
    else:
        return u**n


def expand(u):
    if isinstance(u, Add):
        v = u.args[0]
        return expand(v) + expand(u - v)
    elif isinstance(u, Mul):
        v = u.args[0]
        return expand_product(expand(v), expand(u/v))
    elif isinstance(u, Pow):
        if isinstance(u.exponent, Integer):
            if u.exponent >= Number(2):
                return expand_power(expand(u.base), u.exponent)
            if u.exponent <= Number(-1):
                return Number(1) / expand_power(expand(u.base), abs(u.exponent))
        elif isinstance(u.exponent, Rational):
            largest_int = Number(int(floor(u.exponent.value)))
            m = u.exponent - largest_int
            return expand_product(u.base ** m, expand_power(u.base, largest_int))

    return u


def distribute(u):
    if not isinstance(u, Mul):
        return u

    if not any(isinstance(x, Add) for x in u.args):
        return u

    v = next(x for x in u.args if isinstance(x, Add))
    f = Mul(*[x for x in u.args if x != v])
    s = Number(0)
    for item in v.args:
        s = s + item * f

    return s


# FIXME: Move somewhere more appropriate
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
    return expand(rationalise(u))
