from .numbers import Number, Integer, Rational
from .symbol import Symbol
from .expr import Expression
from .function import Function
from .symbol import Undefined
from .common import convert_type


class Eq(Expression):

    symbol = '='
    commutative = True
    precedence = 5

    def __new__(cls, lhs, rhs, **kwargs):

        lhs = convert_type(lhs)
        rhs = convert_type(rhs)

        obj = super(Eq, cls).__new__(cls, lhs, rhs, **kwargs)
        obj.lhs = lhs
        obj.rhs = rhs

        return obj

    @classmethod
    def simplify(cls, seq):
        return seq

    @property
    def basic_string(self):
        return '{}={}'.format(self.lhs.basic_string, self.rhs.basic_string)

    @property
    def latex(self):
        return self.basic_string

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

        if isinstance(base, Undefined) or isinstance(exponent, Undefined):
            return [Undefined()]

        if base == Number(0):
            if exponent > Number(0):
                return [Number(0)]
            else:
                return [Undefined()]
        elif exponent == Number(1):
            return [base]
        elif base == Number(1):
            return [Number(1)]
        elif exponent == Number(0):
            if base != Number(0):
                return [Number(1)]
            else:  # Range restrictions?
                return [Undefined()]
        elif isinstance(base, Pow):
            return [base.base, (base.exponent * exponent)]
        elif isinstance(base, Mul):
            return [Mul(*[x ** exponent for x in base.args])]
        else:
            return [base, exponent]

    @property
    def basic_string(self):

        string = ''

        for i, arg in enumerate(self.args):
            arg_string = arg.basic_string

            if isinstance(arg, (Add, Mul, Pow)) and arg.precedence <= self.precedence:
                arg_string = '(' + arg_string + ')'

            if i == 0:
                arg_string += '^'

            string += arg_string


        return string

    @property
    def latex(self):
        if isinstance(self.exponent, Number) and self.exponent < 0:  # TODO: sign function?
            return '\\frac{1}{%s}}' % (self**-1).latex
        else:

            base_string = self.base.latex

            if self.exponent == 1:
                return base_string

            if isinstance(base, (Add, Mul)):
                base_string = '(' + base_string + ')'

            return '%s^{%s}' % (base_string, self.exponent.latex)


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

            if isinstance(item, Undefined):
                return [Undefined()]

            if isinstance(item, Number):
                if item != Number(1):
                    coefficient *= item

                    if isinstance(coefficient, Undefined):
                        return [Undefined()]

                continue

            # Mul is commutative
            elif isinstance(item, Mul):
                seq.extend(item.args)
                continue

            base_part = base(item)  # HERE IS THE ISSUE!!!! Fixed?
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

            if len(new_args) == 1 and isinstance(new_args[0], Add):
                new_args = [Add(*[x * coefficient for x in new_args[0].args])]
            else:
                new_args.insert(0, coefficient)
        else:
            if len(new_args) == 0:
                return [coefficient]

        return new_args

    @property
    def basic_string(self):

        string = ''

        for arg in self.args:
            arg_string = arg.basic_string

            if isinstance(arg, (Add, Mul, Pow)) and arg.precedence <= self.precedence:
                    arg_string = '(' + arg_string + ')'

            if arg == -1:
                arg_string = '-'

            string += arg_string

        return string

    @property
    def latex(self):

        num = numerator(self)
        den = denominator(self)

        if den == 1:

            string = ''

            for arg in self.args:
                arg_string = arg.latex

                if isinstance(arg, (Add, Mul, Pow)) and arg.precedence <= self.precedence:
                        arg_string = '(' + arg_string + ')'

                if arg == -1:
                    arg_string = '-'

                string += arg_string

            return string
        else:
            return '\\frac{%s}{%s}' % (num.latex, den.latex)

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

            if isinstance(item, Undefined):
                return [Undefined()]

            # Numbers are added directly to the coefficient
            if isinstance(item, Number):
                if item != Number(0):
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

        if not new_args:
            new_args.append(coefficient)

        return new_args

    @property
    def basic_string(self):

        string = ''

        for i, arg in enumerate(self.args):
            arg_string = arg.basic_string

            if isinstance(arg, (Add, Mul, Pow)) and arg.precedence <= self.precedence:
                arg_string = '(' + arg_string + ')'

            if i != len(self.args) - 1:  # Not the last arg
                arg_string += '+'

            string += arg_string

        return string.replace('+-', '-')

    @property
    def latex(self):
        string = ''

        for i, arg in enumerate(self.args):
            arg_string = arg.latex

            if isinstance(arg, (Add, Mul, Pow)) and arg.precedence <= self.precedence:
                arg_string = '(' + arg_string + ')'

            if i != len(self.args) - 1:  # Not the last arg
                arg_string += '+'

            string += arg_string

        return string.replace('+-', '-')


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
    elif isinstance(u, Pow):
        return u.base
    elif isinstance(u, Number):
        return Undefined()
    else:
        raise ValueError('{} of type {} has fallen through'.format(u, type(u)))


def exponent(u):
    if isinstance(u, (Symbol, Mul, Add, Function)):
        return Number(1)
    if isinstance(u, Pow):
        return u.exponent
    if isinstance(u, (Number)):
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
    elif isinstance(u, Add):
        n, _ = _numer_denom(u)
        return n
    else:
        return u


def denominator(u):

    if isinstance(u, Rational):
        return Number(u.denominator)
    elif isinstance(u, Pow):
        if exponent(u) < 0:
            return base(u) ** abs(exponent(u))
        else:
            return Number(1)
    elif isinstance(u, Mul):
        v = u.args[0]
        return denominator(v) * denominator(u/v)
    elif isinstance(u, Add):
        _, d = _numer_denom(u)
        return d
    else:
        return Number(1)


def _numer_denom(u):

    numer_denom_dict = {}
    for arg in u.args:
        numer = numerator(arg)
        denom = denominator(arg)

        if denom in numer_denom_dict:
            numer_denom_dict[denom] += numer
        else:
            numer_denom_dict[denom] = numer

    denominators, numerators = numer_denom_dict.keys(), numer_denom_dict.values()

    return Add(*[Mul(*(denominators[:i] + [numerators[i]] + denominators[i + 1:])) for i in range(len(numerators))]), Mul(*denominators)