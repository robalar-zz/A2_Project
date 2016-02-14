from .atoms import Base, Atom
from .numbers import Number, Integer, Rational
from .symbol import Symbol


class Expression(Base):

    def __init__(self, *args):
        super(Expression, self).__init__()

        self.args = [Number(x) if isinstance(x, (long, int, float)) else x for x in args]

    def replace(self, old, new):

        self.args = [new if x == old else x for x in self.args]

        try:
            if _sublist(self.args, old.args):
                self.args = _remove_sublist(self.args, old.args)
                self.args.append(new)
        except AttributeError:
            pass

        return self

    def atoms(self, cls=Atom):

        l = [x for x in self.flatten() if isinstance(x, cls)]

        return set(l)

    def flatten(self):
        out = []
        for item in self:
            if isinstance(item, Expression):
                out.extend(item.flatten())
            else:
                out.append(item)

        return out

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


def _sublist(list, sublist):
    n = len(sublist)
    return any((sublist == list[i:i+n]) for i in xrange(len(list)-n+1))

def _remove_sublist(list, sublist):
    for item in sublist:
        try:
            list.remove(item)
        except:
            pass
    return list

def postorder(node):

    if isinstance(node, Expression):
        for arg in node:
            for sub in postorder(arg):
                yield sub

    yield node
