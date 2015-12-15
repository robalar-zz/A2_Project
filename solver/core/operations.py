from atoms import Number, Integer

class Operator(object):
    """ Base class for all arithmetic operators.

    All operators should be derived from this class so they can be identified as an operator.

    Attributes:
        symbol: String representation of the operator.
        precedence: An integer that ranks the 'priority' of the operator, higher precedence operators are evaluated
            first.
        association: A string determining which side of an expression should be evaluated first in the absence of
            brackets and precedence is the same. For example 7 - 4 + 2, left association would yield (7 - 4) + 2 = 5.
            Right association would yield 7 - (4 + 2) = 1.
        commutative: A bool indicating whether the operands can be reveresed while the result remain the same.
            A * B == B * A, commutative = True.
            A / B != B / A, commutative = False.
    """

    symbol = None
    precedence = None
    association = None
    commutative = False


class Pow(Operator):

    symbol = '**'
    precedence = 4
    association = 'right'
    commutative = False

    def __init__(self, left, right):
        pass


class Mul(Operator):

    symbol = '*'
    precedence = 3
    association = 'left'
    commutative = True

    def __init__(self, left, right):
        pass



class Div(Operator):

    symbol = '/'
    precedence = 3
    association = 'left'
    commutative = False

    def __init__(self, left, right):
        pass


class Add(Operator):

    symbol = '+'
    precedence = 2
    association = 'left'
    commutative = True

    def __new__(cls, args):
        if all(isinstance(n, Number) for n in args):
            total = Integer(0)
            for n in args:
                total += n
            return total


class Sub(Operator):

    symbol = '-'
    precedence = 2
    association = 'left'
    commutative = False

    def __init__(self, left, right):
        pass


class UMin(Operator):

    symbol = '-u'
    precedence = 4
    association = 'right'
    commutative = False


def is_operator(token, op=Operator):
    """ Checks whether a token is an operator or not.

    Args:
        token: Token to be tested.
        op: Operator to test token against, defaults to Operator base class.
    Returns:
        Bool indicating whether token was an operator.

    >>> is_operator(Mul)
    True
    >>> is_operator('x')
    False
    >>> is_operator(Div, Div)
    True
    >>> is_operator(Pow, Add)
    False
    """

    try:
        if not issubclass(token, op):
            return False
        return True
    except TypeError:
        # token is not a class (or operator)
        return False


def is_commutative_operator(token):
    """
    >>> is_commutative_operator(Mul)
    True
    >>> is_commutative_operator('x')
    False
    >>> is_commutative_operator(Pow)
    False
    """
    return is_operator(token) and token.commutative
