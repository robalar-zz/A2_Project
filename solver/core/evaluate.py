from .numbers import Rational, Integer, Number, Undefined

def evaluate_add(p, q):
    if not isinstance(p, Number) or not isinstance(q, Number):
        raise ValueError('p and q must be Number instances')

    if isinstance(p, Undefined) or isinstance(q, Undefined):
        return Undefined()
    else:
        return Number(p.value + q.value)


def evaluate_mul(p, q):
    if not isinstance(p, Number) or not isinstance(q, Number):
        raise ValueError('p and q must be Number instances')

    if isinstance(p, Undefined) or isinstance(q, Undefined):
        return Undefined()
    else:
        return Number(p.value * q.value)

def evaluate_power(v, n):
    """ Evaluates an integer power.

        Args:
            v: Base of the power, must be a Rational or Integer
            n: Exponential of the power, must be an Integer
        Returns:
            The evaluated power, or Undefined
        Raises:
            ValueError: if n is not an Integer or v is not an Integer or Rational
    """

    if not isinstance(n, Integer):
        raise ValueError('n must be an integer')

    if not isinstance(v, (Integer, Rational)):
        raise ValueError('v must be an integer or rational')

    # v != 0 or v != 0/n
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
        elif n < Number(-1):  # (a/b)^-4 -> (b/a)^4 i.e (1/2)^-2 = (2/1)^2 = 4, 4^-3 = (4/1)^-3 = (1/4)^3 = 1/64
            if isinstance(v, Integer):
                return Rational(1, evaluate_power(v, abs(n)))
            if isinstance(v, Rational):
                return evaluate_power(Rational(v.denominator, v.numerator), abs(n))
    # v == 0
    else:
        if n >= Number(1):  # 0^a -> 0, a >= 1
            return Number(0)
        elif n <= Number(0): # 0^a -> undefined, a <= 0 i.e 0^-2 = (1/0)^2 = undefined
            return Undefined()