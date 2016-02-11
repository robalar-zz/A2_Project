from .numbers import Rational, Integer, Number, Undefined

def evaluate_add():
    raise NotImplementedError

def evaluate_mul():
    raise NotImplementedError

def evaluate_power(v, n):
    """ Evaluates an integer power.
    """

    if not isinstance(n, Integer):
        raise ValueError('n must be an integer')

    if (isinstance(v, Rational) and v.numerator != 0) or (isinstance(v, Integer) and v != Number(0)):
        if n > Number(0):  # Power is positive i.e 3^2, (1/2)^3
            return Number(v.value ** n.value)
        elif n == Number(0):  # x^0 -> 1, x != 0
            return Number(1)
        elif n == Number(-1):  # (a/b)^-1 -> b/a i.e (1/2)^-1 = 2/1 = 2, 3^-1 = (3/1)^-1 = 1/3
            if isinstance(v, Integer):
                return Rational(1, v.value)
            if isinstance(v, Rational):
                return Rational(v.denominator, v.numerator)
        elif n < Number(-1):
            if isinstance(v, Integer):
                return Rational(1, evaluate_power(v, abs(n)))
            if isinstance(v, Rational):
                return evaluate_power(Rational(v.denominator, v.numerator), abs(n))
    else:
        if n >= Number(1):
            return Number(0)
        elif n <= Number(0):
            return Undefined()