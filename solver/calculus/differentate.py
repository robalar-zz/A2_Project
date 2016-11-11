from ..core.numbers import Number
from ..core.operations import Pow, Add, Mul, free_of, base, exponent, Eq
from ..core.function import Function
from ..core.symbol import free_symbols

class d(Function):

    name = 'd/d'
    nargs = 2

    def __init__(self, u, x):
        self.name += str(x)
        super(d, self).__init__(u, x)


# TODO: Move to more appropriate place
class ln(Function):

    name = 'ln'
    nargs = 1

    @property
    def derivative(self):
        return lambda x: 1/x

    def __init__(self, x):
        super(ln, self).__init__(x)

class e(Function):

    name = 'e'
    nargs = 1

    @property
    def derivative(self):
        return lambda x: e(x)

    def __init__(self, x):
        super(e, self).__init__(x)
###


def derivative(u, x):
    if u == x:
        return Number(1)

    elif isinstance(u, Eq):
        v = u.lhs - u.rhs
        syms = free_symbols(u)

        if len(syms) == 2:
            y = (syms - {x}).pop()
            return -derivative(v, x)/derivative(v, y)
        elif len(syms) == 1:
            return derivative(v, x)
        else:
            raise NotImplementedError('Implicit derivatives for > 2 variables is not supported')

    elif isinstance(u, Pow):
        w = exponent(u)
        v = base(u)
        return w * v **(w-1) * derivative(v, x) + derivative(w, x) * v**w * ln(v)

    elif isinstance(u, Add):
        v = u.args[0]
        return derivative(v, x) + derivative(u-v, x)

    elif isinstance(u, Mul):
        v = u.args[0]
        return derivative(v, x) * (u/v) + v * derivative(u/v, x)

    elif isinstance(u, Function):

        v = u.args[0]

        if u.derivative is not None:
            return u.derivative(v) * derivative(v, x)
        else:
            return d(u, x) * derivative(v, x)

    elif free_of(u, x):
        return Number(0)

    return d(u, x)
