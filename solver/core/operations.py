from .atoms import Number, Atom
from .symbol import Symbol

from operator import mul

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

    def __new__(cls, *args):

        obj = super(Operator, cls).__new__(cls)

        # FIXME
        # python_nums = [i for i in args if isinstance(i, (float, int, long))]
        # args = [i for i in args if i not in python_nums]

        # print python_nums

        return obj

    # TODO: Find a less 'hacky' way to do this?
    def __add__(self, other):
        return Add(self, other)

    def __mul__(self, other):
        return Mul(self, other)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.args)

    def get_atoms(self, type=Atom):
        return [arg for arg in self.args if isinstance(arg, type)]


class Eq(Operator):

    symbol = '='

    def __new__(cls, *args):
        pass


class Pow(Operator):

    symbol = '**'
    precedence = 4
    association = 'right'
    commutative = False

    def __new__(cls, *args):
        obj = super(Pow, cls).__new__(cls, *args)

        if len(args) != 2:
            raise ValueError('Pow must have 2 args (base, exponent)')

        obj.args = list(args)

        # x ** 1 = x
        if obj.args[1] == Number(1):
            return obj.args[0]

        # If all the arguments are numbers just evaluate
        if all(isinstance(arg, Number) for arg in obj.args):
            return args[0] ** args[1]

        # x**0 = 1, x != 0
        if obj.args[1] == Number(0) and obj.args[0] != Number(0):
            return Number(1)

        return obj


class Mul(Operator):

    symbol = '*'
    precedence = 3
    association = 'left'
    commutative = True

    def __new__(cls, *args):
        obj = super(Mul, cls).__new__(cls, *args)
        obj.args = list(args)

        # x * 0 = 0
        if Number(0) in obj.args:
            return Number(0)

        # x * 1 = x
        if Number(1) in obj.args:
            obj.args.remove(Number(1))

        # Folding nested Mul's
        for item in [arg for arg in args if isinstance(arg, Mul)]:
            obj.args += item.args
            obj.args.remove(item)

        # If all the arguments are numbers just evaluate
        if all(isinstance(arg, Number) for arg in args):
            return reduce(mul, args, Number(1))

        # Simplifying powers
        obj.args = [x**Number(1) if isinstance(x, Symbol) else x for x in obj.args]  # x -> x**1

        powers = [power for power in obj.args if isinstance(power, Pow)]
        obj.args = [x for x in obj.args if x not in powers]
        for power in powers:
            same_base = [other for other in powers if other.args[0] == power.args[0]]

            if len(same_base) < 2:
                continue

            final = Pow(same_base[0].args[0], Add(*[x.args[1] for x in same_base]))

            powers = [x for x in powers if x not in same_base]

            powers.append(final)

        obj.args.extend(powers)

        # If there's only one arg return that
        if len(obj.args) == 1:
            return obj.args[0]

        return obj

    def get_coefficient(self):
        return [i for i in self.args if isinstance(i, Number)][0]


class Div(Operator):

    symbol = '/'
    precedence = 3
    association = 'left'
    commutative = False

    def __new__(cls, numerator, denominator):
        return numerator * denominator ** -1


class Add(Operator):

    symbol = '+'
    precedence = 2
    association = 'left'
    commutative = True

    def __new__(cls, *args):
        obj = super(Add, cls).__new__(cls)
        obj.args = list(args)

        # Fold nested Add's
        for item in [arg for arg in args if isinstance(arg, Add)]:
            obj.args += item.args
            obj.args.remove(item)

        # If all args are numbers just evaluate
        if all(isinstance(arg, Number) for arg in args):
            return sum(args, Number(0))

        # x + 0 = x
        if Number(0) in obj.args:
            obj.args.remove(Number(0))

        # Simplifying symbol addition
        symbols = [sym for sym in obj.args if isinstance(sym, Symbol)]
        obj.args = [x for x in obj.args if x not in symbols]

        for symbol in symbols:
            same_symbols = [other for other in symbols if other == symbol]

            if len(same_symbols) < 2:
                continue

            coefficient = len(same_symbols)
            final = coefficient * symbol
            symbols = [x for x in symbols if x not in same_symbols]
            symbols.append(final)

        obj.args.extend(symbols)

        # Simplifying multiplied symbols
        muls = [op for op in obj.args if isinstance(op, Mul) and (any(isinstance(sym, Symbol) for sym in op.args))]
        obj.args = [x for x in obj.args if x not in muls]

        for multiplication in muls:
            same_symbols = [other for other in muls if other.get_atoms(Symbol) == multiplication.get_atoms(Symbol)]

            if len(same_symbols) < 2:
                continue

            coefficients = [m.get_coefficient() for m in same_symbols]

            final_coeff = sum(coefficients, Number(0))
            final_symbols = same_symbols[0].get_atoms(Symbol)
            final = Mul(final_coeff, *final_symbols)

            muls = [x for x in muls if x not in same_symbols]
            muls.append(final)

        obj.args.extend(muls)

        # If there's only one arg return that
        if len(obj.args) == 1:
            return obj.args[0]

        return obj


class Sub(Operator):

    symbol = '-'
    precedence = 2
    association = 'left'
    commutative = False

    def __new__(cls, left, right):
        return left + (-1 * right)



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
