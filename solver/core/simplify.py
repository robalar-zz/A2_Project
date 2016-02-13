from .numbers import Integer, Rational, Undefined, Number
from .symbol import Symbol
from .operations import Pow, Mul, Add, base, exponent, term, const
from .subs import _map
from .evaluate import *
from .order import isordered

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
            elif isinstance(u, Pow):
                v = simp_rec(u.args[0])
                if isinstance(v, Undefined):
                    return Undefined()
                else:
                    return evaluate_power(v, u.args[1])

    v = simp_rec(u)
    if isinstance(v, Undefined):
        return Undefined
    else:
        return simplify_rational(v)


def simplify_integer_power(v, w):
    if not isinstance(w, Integer):
        raise ValueError('w must be a Integer')

    # SINTPOW-1
    if isinstance(v, (Integer, Rational)):  # if both are integers
        return simplify_rne(Pow(v, w))
    # SINTPOW-2
    elif w == Number(0):  # x^0 -> 1
        return Number(1)
    # SINTPOW-3
    elif w == Number(1):  # x^1 -> x, x != 0 (already implied from simplify_power)
        return v
    # SINTPOW-4
    elif isinstance(v, Pow):  # If base is also power then, (x^a)^b -> x^(a*b)
        r = v.base
        s = v.exponent
        p = simplify_product(Mul(s, w))

        if isinstance(p, Integer):  # Can possibly be simplified
            return simplify_integer_power(r, p)
        else:  # Can't be simplified
            return Pow(r, p)
    # SINTPOW-5
    elif isinstance(v, Mul):  # (a * b * c^2)^2 -> a^2 * b^2 * c^4
        r = _map(simplify_integer_power, v, w)
        return r
    # SINTPOW-6
    else:
        return Pow(v, w)


def simplify_power(u):
    if not isinstance(u, Pow):
        raise ValueError('u must be a Pow')

    v = u.base
    w = u.exponent

    # SPOW-1
    if isinstance(v, Undefined) or isinstance(w, Undefined):  # Undefined^a -> Undefined, a^Undefined -> Undefined
        return Undefined()
    # SPOW-2
    elif v == Number(0):
        if isinstance(w, Number) and w > Number(0):  # Power is positive integer or rational
            return Number(0)
        else:
            return Undefined()
    # SPOW-3
    elif v == Number(1):
        return Number(1)
    # SPOW-4
    elif isinstance(w, Integer):
        return simplify_integer_power(v, w)
    # SPOW-5
    else:
        return u


def merge_products(p, q):
    if not isinstance(p, list) and not isinstance(p, list):
        raise ValueError('p and q must be lists')
    # MMUL-1
    if not q:
        return p
    # MMUL-2
    elif not p:
        return q
    # MMUL-3
    else:
        h = _simplify_product_rec([p[0], q[0]])
        # MMUL-3-1
        if not h:
            return merge_products(p[1:], q[1:])
        # MMUL-3-2
        elif len(h) == 1:
            v = merge_products(p[1:], q[1:])
            v.insert(0, h[0])
            return v
        # MMUL-3-3
        elif h == [p[0], q[0]]:
            v = merge_products(p[1:], q)
            v.insert(0, p[0])
            return v
        elif h == [q[0], p[0]]:
            v = merge_products(p, q[1:])
            v.insert(0, q[0])
            return v

def _simplify_product_rec(l):
    if not len(l) >= 2:
        ValueError('u must be a list with len >= 2')
    if len(l) == 2:
        # SMULREC-1
        if not isinstance(l[0], Mul) and not isinstance(l[1], Mul):
            # SMULREC-1-1
            if isinstance(l[0], Number) and isinstance(l[1], Number):
                p = simplify_rne(Mul(l[0], l[1]))
                if p == Number(1):
                    return []
                else:
                    return [p]
            # SMULREC-1-2
            elif l[0] == Number(1):
                return [l[1]]
            elif l[1] == Number(1):
                return [l[0]]
            # SMULREC-1-3
            elif base(l[0]) == base(l[1]):
                s = simplify_sum(Add(exponent(l[0]), exponent(l[1])))
                p = simplify_power(Pow(base(l[0]), s))

                if p == Number(1):
                    return []
                else:
                    return [p]
            # SMULREC-1-4
            elif isordered(l[1], l[0]):
                return [l[1], l[0]]
            # SMULREC-1-5
            else:
                return l

        # SMULREC-2
        if isinstance(l[0], Mul) or isinstance(l[1], Mul):
            # SMULREC-2-1
            if isinstance(l[0], Mul) and isinstance(l[1], Mul):
                return merge_products(l[0].args, l[1].args)
            # SMULREC-2-2
            if isinstance(l[0], Mul):
                return merge_products(l[0].args, [l[1]])
            if isinstance(l[1], Mul):
                return merge_products([l[0]], l[1].args)
    # SMULREC-3
    if len(l) > 2:
        w = _simplify_product_rec(l[1:])
        # SMULREC-3-1
        if isinstance(l[0], Mul):
            return merge_products(l[0].args, w)
        # SMULREC-3-2
        else:
            return merge_products([l[0]], w)


def simplify_product(u):

    if not isinstance(u, Mul):
        raise ValueError('u must be a Mul instance')

    args = u.args

    # SMUL-1
    if any(isinstance(v, Undefined) for v in args):
        return Undefined()
    # SMUL-2
    if any(v == Number(0) for v in args):
        return Number(0)
    # SMUL-3
    if len(args) == 1:
        return args[0]
    # SMUL-4
    v = _simplify_product_rec(args)
    if len(v) == 1:
        return v[0]
    if len(v) >= 2:
        return Mul(*v)
    if len(v) == 0:
        return Number(1)


def merge_sums(p, q):
    # MADD-1
    if not p:
        return q
    # MADD-2
    if not q:
        return p
    # MADD-3
    else:
        h = _simplify_sum_rec([p[0], q[0]])
        # MADD-3-1
        if not h:
            return merge_sums(p[1:], q[1:])
        # MADD-3-2
        if len(h) == 1:
            v = merge_sums(p[1:], q[1:])
            v.insert(0, h[0])
            return v
        # MADD-3-3
        if h == [p[0], p[0]]:
            v = merge_sums(p[1:], q)
            v.insert(0, p[0])
            return v
        if h == [q[0], p[0]]:
            v = merge_sums(p, q[1:])
            v.insert(0, q[0])
            return v


def _simplify_sum_rec(l):
    if not len(l) >= 2:
        ValueError('u must be a list with len >= 2')

    if len(l) == 2:
        # SADDREC-1
        if not isinstance(l[0], Add) and not isinstance(l[1], Add):
            # SADDREC-1-1
            if isinstance(l[0], Number) and isinstance(l[1], Number):
                p = simplify_rne(Add(l[0], l[1]))
                if p == Number(0):
                    return []
                else:
                    return [p]
            # SADDREC-1-2
            elif l[0] == Number(0):
                return [l[1]]
            elif l[1] == Number(0):
                return [l[0]]
            # SADDREC-1-3
            elif term(l[0]) == term(l[1]):
                s = simplify_sum(Add(const(l[0]), const(l[1])))
                p = simplify_product(Mul(s, term(l[0])))
                if p == Number(0):
                    return []
                else:
                    return [p]
            # SADDREC-1-4
            elif isordered(l[1], l[0]):
                return [l[1], l[0]]
            # SADDREC-1-5
            else:
                return l

        # SADDREC-2
        if isinstance(l[0], Add) or isinstance(l[1], Add):
            # SADDREC-2-1
            if isinstance(l[0], Add) and isinstance(l[1], Add):
                return merge_sums(l[0].args, l[1].args)
            if isinstance(l[0], Add):
                return merge_sums(l[0].args, [l[1]])
            if isinstance(l[1], Add):
                return merge_sums([l[0]], l[1].args)

        # SADDREC-3
        if len(l) > 2:
            w = _simplify_sum_rec(l[1:])
            if isinstance(l[0], Add):
                return merge_products(l[0].args, w)
            else:
                return merge_products([l[0]], w)


def simplify_sum(u):

    if not isinstance(u, Add):
        raise ValueError('u must be a Add instance')

    args = u.args

    # SADD-1
    if any(isinstance(v, Undefined) for v in args):
        return Undefined()
    # SADD-2
    elif len(args) == 1:
        return args[0]
    # SADD-3
    else:
        v = _simplify_sum_rec(args)
        if len(v) == 1:
            return v[0]
        elif len(v) >= 2:
            return Add(*v)
        elif not v:
            return Number(0)


def simplify_function(u):
    raise NotImplementedError


def auto_simplify(u):
    if isinstance(u, (Integer, Symbol)):
        return u
    elif isinstance(u, Rational):
        return simplify_rational(u)
    else:
        v = _map(auto_simplify, u)
        if isinstance(v, Pow):
            return simplify_power(v)
        elif isinstance(v, Mul):
            return simplify_product(v)
        elif isinstance(v, Add):
            return simplify_sum(v)
        else:
            return simplify_function(v)
