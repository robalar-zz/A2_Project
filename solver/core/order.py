from .numbers import Number, Integer
from .symbol import Symbol
from .operations import Mul, Add, Pow, base, exponent, term
from .expr import subexpressions
from .function import Function

import itertools


def isordered(u, v):
    # O-1
    if isinstance(u, Number) and isinstance(v, Number):
        return u < v

    #O-2
    if isinstance(u, Symbol) and isinstance(v, Symbol):
        return u.name < v.name

    #O-3
    if (isinstance(u, Mul) and isinstance(v, Mul)) or (isinstance(u, Add) and isinstance(v, Add)):

        m = len(u.args) - 1
        n = len(v.args) - 1

        if u.args[m] != v.args[n]:
            return isordered(u.args[m], v.args[n])

        k = zip(u.args[::-1], v.args[::-1]) # zip last to last

        for j in k:
            if j[0] != j[1]:
                return isordered(j[0], j[1])

        if all(j[0] == j[1] for j in k):
            return m < n

    #O-4
    if isinstance(u, Pow) and isinstance(v, Pow):
        if base(u) != base(v):
            return isordered(base(u), base(v))
        if base(u) == base(u):
            return isordered(exponent(u), exponent(v))

    #O-6
    if isinstance(u, Function) and isinstance(v, Function):
        if u.name != v.name:
            return u.name < u.name
        else:
            m = len(u.args) - 1
            n = len(v.args) - 1

            k = zip(u.args, v.args)  # zip first to first

            for j in k:
                if j[0] != j[1]:
                    return isordered(j[0], j[1])

            if all(j[0] == j[1] for j in k):
                return m < n

    #O-7
    if isinstance(u, Number) and not isinstance(v, Number):
        return True

    #O-8
    if isinstance(u, Mul) and isinstance(v, (Pow, Add, Symbol, Function)):
        return isordered(u, Mul(v))

    #O-9
    if isinstance(u, Pow) and isinstance(v, (Add, Symbol, Function)):
        return isordered(u, Pow(v, Number(1)))

    #O-10
    if isinstance(u, Add) and isinstance(v, (Symbol, Function)):
        return isordered(u, Add(v))

    #O-12
    if isinstance(u, Function) and isinstance(v, Symbol):
        if u.name == v.name:
            return False
        else:
            return u.name < v.name

    #O-13
    return not isordered(v, u)


def is_asae(u):
    # ASAE-1
    if isinstance(u, Integer):
        return True

    # ASAE-3
    if isinstance(u, Symbol):
        return True

    # ASAE-4
    if isinstance(u, Mul) and len(u.args) >= 2:

        result = all(is_asae(v) and v != Number(1) and v != Number(0) and not isinstance(v, Mul) for v in u.args)
        result = result and len(subexpressions(u, Number)) <= 1

        for i, j in itertools.permutations(u.args, 2):
            ui = u.args.index(i)
            uj = u.args.index(j)
            result = result and base(i) != base(j)

            if ui < uj:
                result = result and isordered(i, j)

        return result

    # ASAE-5
    if isinstance(u, Add) and len(u.args) >= 2:
        result = all(is_asae(v) and v != Number(0) and not isinstance(v, Add) for v in u.args)
        result = result and len(subexpressions(u, Number)) <= 1

        for i, j in itertools.permutations(u.args, 2):
            ui = u.args.index(i)
            uj = u.args.index(j)
            result = result and term(i) != term(j)

            if ui < uj:
                result = result and isordered(i, j)

        return result

    # ASAE-6
    if isinstance(u, Pow):
        result = all(is_asae(v) for v in u.args)
        result = result and not (exponent(u) == Number(0) or exponent(u) == Number(1))
        if isinstance(exponent(u), Integer):
            result = result and is_asae(base(u)) and not isinstance(base(u), Number) and not isinstance(base(u), Mul) \
                     and not isinstance(base(u), Pow)
        if not isinstance(exponent(u), Integer):
            result = result and (is_asae(base(u)) and not (base(u) == Number(0) or base(u) == Number(1)))
        return result

    return False
