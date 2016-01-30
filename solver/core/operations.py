from .numbers import Number
from .symbol import Symbol
from .expr import Expression

from operator import mul

# TODO: Separate into functions?
# TODO: Separate into different files?


class Eq(Expression):

    symbol = '='

    def __new__(cls, *args):
        raise NotImplementedError


class Pow(Expression):

    symbol = '**'
    precedence = 4
    association = 'right'
    commutative = False

    def __new__(cls, *args):
        obj = Expression.__new__(cls, *args)

        if len(args) != 2:
            raise ValueError('Pow must have 2 args (base, exponent)')

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


class Mul(Expression):

    symbol = '*'
    precedence = 3
    association = 'left'
    commutative = True

    def __new__(cls, *args):
        obj = Expression.__new__(cls, *args)

        # x * 0 = 0
        #if Number(0) in obj.args:
            #return Number(0)

        # x * 1 = x
        #if Number(1) in obj.args:
            #obj.args.remove(Number(1))

        # Folding nested Mul's
        for item in [arg for arg in args if isinstance(arg, Mul)]:
            obj.args += item.args
            obj.args.remove(item)

        # If all the arguments are numbers just evaluate
        if all(isinstance(arg, Number) for arg in args):
            return reduce(mul, args, Number(1))

        # Simplifying powers
        #obj.args = [x**Number(1) if isinstance(x, Symbol) else x for x in obj.args]  # x -> x**1

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


class Add(Expression):

    symbol = '+'
    precedence = 2
    association = 'left'
    commutative = True

    def __new__(cls, *args):
        obj = Expression.__new__(cls, *args)

        # Fold nested Add's
        for item in [arg for arg in args if isinstance(arg, Add)]:
            obj.args += item.args
            obj.args.remove(item)

        # If all args are numbers just evaluate
        if all(isinstance(arg, Number) for arg in args):
            return sum(args, Number(0))

        # x + 0 = x
        #if Number(0) in obj.args:
            #obj.args.remove(Number(0))

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

        # Simplifying multiplied symbols FIXME
        """
        obj.args = [Number(1)*x if isinstance(x, Symbol) else x for x in obj.args]

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

        obj.args.extend(muls)"""

        # If there's only one arg return that
        if len(obj.args) == 1:
            return obj.args[0]

        return obj
