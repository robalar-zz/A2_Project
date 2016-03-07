from ..core.numbers import Number
from ..core.operations import Pow, base, exponent, Add, Mul
from ..core.expr import free_of
from ..core.function import Function
from ..trigonometry.functions import *

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

    def __init__(self, x):
        super(ln, self).__init__(x)

class e(Function):

    name = 'e'
    nargs = 1

    def __init__(self, x):
        super(e, self).__init__(x)
###


def derivative(u, x):
    if u == x:
        return Number(1)

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
        if isinstance(u, sin):
            v = u.args[0]
            return cos(v) * derivative(v, x)

        elif isinstance(u, cos):
            v = u.args[0]
            return -sin(v) * derivative(v, x)

        elif isinstance(u, tan):
            v = u.args[0]
            return sec(v)**2 * derivative(v, x)

        elif isinstance(u, e):
            v = u.args[0]
            return u * derivative(v, x)

        else:
            v = u.args[0]
            return d(u, x) * derivative(v, x)

    elif free_of(u, x):
        return Number(0)

    return d(u, x)
