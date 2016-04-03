from .numbers import Number, Integer, Rational, Undefined
from .symbol import Symbol
from .expr import Expression
from .function import Function


class Eq(Expression):

    symbol = '='

    def __new__(cls, lhs, rhs):
        return super(Eq, cls).__new__(lhs, rhs)


class NEq(Eq):

    symbol = '!='

class LessThan(Eq):

    symbol = '<'


# TODO define all binary ops
class Not(Expression):

    symbol = '~'


class And(Expression):

    symbol = '/\\'


class Or(Expression):

    symbol = '\\/'


class Pow(Expression):

    symbol = '^'
    precedence = 4
    association = 'right'
    commutative = False
    
    @property
    def base(self):
        return self.args[0]

    @property
    def exponent(self):
        return self.args[1]

    @classmethod
    def simplify(cls, seq):
        base = seq[0]
        exponent = seq[1]

        if base == Number(0):
            if exponent > Number(0):
                return [Number(0)]
            else:
                return [Undefined()]
        elif exponent == Number(1):
            return [base]
        elif base == Number(1):
            return [Number(1)]
        else:
            return [base, exponent]


class Mul(Expression):

    symbol = '*'
    precedence = 3
    association = 'left'
    commutative = True

    @classmethod
    def simplify(cls, seq):
        coefficient = Number(1)
        terms = {}

        for item in seq:
            if isinstance(item, Number) and item != Number(1):
                coefficient *= item

                if isinstance(coefficient, Undefined):
                    return [Undefined()]

                continue

            # Mul is commutative
            elif isinstance(item, Mul):
                seq.extend(item.args)
                continue

            base_part = base(item)
            exponent_part = exponent(item)


            if base_part in terms:
                terms[base_part] += exponent_part
            else:
                terms[base_part] = exponent_part

        if coefficient == Number(0):
            return [Number(0)]

        new_args = []

        for base_part, exponent_part in terms.items():

            if exponent_part == Number(1):
                new_args.append(base_part)
            elif base_part == Number(1):
                new_args.append(Number(1))
            else:
                new_args.append(Pow(base_part, exponent_part))

        if coefficient != Number(1):
            new_args.insert(0, coefficient)

        return new_args


class Add(Expression):

    symbol = '+'
    precedence = 2
    association = 'left'
    commutative = True

    @classmethod
    def simplify(cls, seq):
        coefficient = Number(0)
        terms = {}

        for item in seq:
            # Numbers are added directly to the coefficient
            if isinstance(item, Number) and item != Number(0):
                if isinstance(item, Undefined):
                    return [item]  # Sums containing Undefined are also Undefined.
                else:
                    coefficient += item
                continue

            # Addition is commutative
            elif isinstance(item, Add):
                seq.extend(item.args)
                continue

            coeff_part = const(item)
            term_part = term(item)


            if term_part in terms:
                terms[term_part] += coeff_part
            else:
                terms[term_part] = coeff_part

        new_args = []

        for term_part, coeff_part in terms.items():

            # 0 * x = 0
            if coeff_part == Number(0):
                continue
            # 1 * x = x
            elif coeff_part == Number(1):
                new_args.append(term_part)
            else:
                # Commutativity
                if isinstance(term_part, Mul):
                    m = Mul(coeff_part, *term_part.args)
                    new_args.append(m)
                else:
                    new_args.append(Mul(coeff_part, term_part))

        if coefficient != Number(0):
            new_args.insert(0, coefficient)

        return new_args



def free_of(u, t):
    if u == t:
        return False
    elif isinstance(u, (Symbol, Integer, Rational)):
        return True
    else:
        for operand in u.args:
            if not free_of(operand, t):
                return False
        return True


def free_of_set(u, t_set):
    return all(free_of(u, t) for t in t_set)


def subexpressions(expression, types=Expression):
    """ Returns the sub-expressions present in an expression.
    """
    try:
        return [x for x in expression.args if isinstance(x, types)]
    except AttributeError:
        return []


def base(u):
    if isinstance(u, (Symbol, Mul, Add, Function)):
        return u
    if isinstance(u, Pow):
        return u.base
    if isinstance(u, Number):
        return Undefined()


def exponent(u):
    if isinstance(u, (Symbol, Mul, Add, Function)):
        return Number(1)
    if isinstance(u, Pow):
        return u.exponent
    if isinstance(u, Number):
        return Undefined()


def term(u):
    # Assumes that the constant (number) is the first arg, as it should be with the correct ordering,
    # and there is only one constant

    if isinstance(u, (Symbol, Add, Pow, Function)):
        return u
    if isinstance(u, Mul) and isinstance(u.args[0], Number):
        return Mul(*u.args[1:])
    if isinstance(u, Mul) and not isinstance(u.args[0], Number):
        return u
    if isinstance(u, Number):
        return Undefined()


def const(u):
    if isinstance(u, (Symbol, Add, Pow, Function)):
        return Number(1)
    if isinstance(u, Mul) and isinstance(u.args[0], Number):
        return u.args[0]
    if isinstance(u, Mul) and not isinstance(u.args[0], Number):
        return Number(1)
    if isinstance(u, Number):
        return Undefined()


def numerator(u):
    if isinstance(u, Rational):
        return Number(u.numerator)  # FIXME: Number conversion should be handled in Rational
    elif isinstance(u, Pow):
        if exponent(u) < Number(0):
            return Number(1)
        else:
            return u
    elif isinstance(u, Mul):
        v = u.args[0]
        return numerator(v) * numerator(u/v)
    else:
        return u


def denominator(u):
    if isinstance(u, Rational):
        return Number(u.denominator)
    elif isinstance(u, Pow):
        if exponent(u) < Number(0):
            return base(u) ** abs(exponent(u))
        else:
            return Number(1)
    elif isinstance(u, Mul):
        v = u.args[0]
        return denominator(v) * denominator(u/v)
    else:
        return Number(1)