from .numbers import Number
from .symbol import Symbol
from .operations import Mul, Add, Pow, base, exponent

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

    #O-7
    if isinstance(u, Number) and not isinstance(v, Number):
        return True

    #O-8
    if isinstance(u, Mul) and isinstance(v, (Pow, Add, Symbol)):
        return isordered(u, Mul(v))

    #O-9
    if isinstance(u, Pow) and isinstance(v, (Add, Symbol)):
        return isordered(u, Pow(v, Number(1)))

    #O-10
    if isinstance(u, Add) and isinstance(v, (Symbol)):
        return isordered(u, Add(v))

    #O-13
    return not isordered(v, u)
