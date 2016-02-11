from .numbers import Integer, Rational, Undefined, Number
from .symbol import Symbol
from .operations import Pow, Mul, Add
from .subs import _map
from .evaluate import *

from fractions import gcd

def simplify_rational(u):
    if isinstance(u, Integer):
        return u
    elif isinstance(u, Rational):
        n = u.numerator
        d = u.denominator

        integer_quotent, integer_remainder = divmod(n, d)

        if integer_remainder == 0:
            return integer_quotent
        else:
            g = gcd(n, d)
            if d > 0:
                new_numerator, _ = divmod(n, g)
                new_denominator, _ = divmod(d, g)
                return Rational(new_numerator, new_denominator)
            elif d < 0:
                new_numerator, _ = divmod(-n, g)
                new_denominator, _ = divmod(-d, g)
                return Rational(new_numerator, new_denominator)


def simplify_rne(u):
    def simp_rec(u):
        if isinstance(u, Integer):
            return u

        elif isinstance(u, Rational):
            if u.denominator == 0:
                return Undefined()

        elif len(u.args) == 1:
            v = simp_rec(u.args[0])
            if isinstance(v, Undefined):
                return Undefined()
            elif isinstance(v, Add):
                return v

        elif len(u.args) == 2:
            if isinstance(u, (Add, Mul)):
                v = simp_rec(u.args[0])
                w = simp_rec(u.args[1])

                if isinstance(v, Undefined) or isinstance(v, Undefined):
                    return Undefined()

                else:
                    if isinstance(u, Add):
                        return evaluate_add(v, w)
                    if isinstance(u, Mul):
                        return evaluate_mul(v, w)
            else:
                v = simp_rec(u.args[0])
                if isinstance(v, Undefined):
                    return Undefined()
                else:
                    return evaluate_power(v, u.args[1])



def simplify_integer_power(v, w):
    # SINTPOW-1
    if isinstance(v, (Integer, Rational)):  # if both are integers
        return simplify_rne(Pow(v, w))
    # SINTPOW-2
    if w == Number(0):  # x^0 -> 1
        return Number(1)
    # SINTPOW-3
    if w == Number(1):  # x^1 -> x, x != 0 (already implied from simplify_power)
        return v
    # SINTPOW-4
    if isinstance(v, Pow):  # If base is also power then, (x^a)^b -> x^(a*b)
        r = v.base
        s = v.exponent
        p = simplify_product(Mul(s, w))

        if isinstance(p, Integer):
            return simplify_integer_power(r, p)
        else:
            return Pow(r, p)



def simplify_power(u):
    v = u.base
    w = u.exponent

    if isinstance(v, Undefined) or isinstance(w, Undefined):
        return Undefined()
    elif v == Number(0):
        if isinstance(w, Number) and w > Number(0):
            return Number(0)
        else:
            return Undefined()
    elif isinstance(w, Integer):
        return simplify_integer_power(v, w)
    else:
        return u

def simplify_product(u):
    raise NotImplementedError

def simplify_sum(u):
    raise NotImplementedError

def simplify_function(u):
    raise NotImplementedError


def auto_simplify(u):
    if isinstance(u, (Integer, Symbol)):
        return u
    elif isinstance(u, Rational):
        return simplify_rational(u)
    else:
        v = _map(auto_simplify, u)
        if isinstance(u, Pow):
            return simplify_power(u)
        elif isinstance(u, Mul):
            return simplify_product(u)
        elif isinstance(u, Add):
            return simplify_sum(u)
        else:
            return simplify_function(u)
