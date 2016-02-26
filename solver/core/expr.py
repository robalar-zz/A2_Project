from .atoms import Base, Atom
from .numbers import Number, Integer, Rational
from .symbol import Symbol


class Expression(Base):

    def __init__(self, *args):
        super(Expression, self).__init__()

        self.args = [Number(x) if isinstance(x, (long, int, float)) else x for x in args]

        if any(isinstance(x, (long, int, float)) for x in self.args):
            o = [x for x in args if isinstance(x, (long, int, float))]
            raise ValueError('Tried to create expression with non-basic types: {}'.format(o))



    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, str(self.args)[1:-1])

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.args == other.args
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


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
