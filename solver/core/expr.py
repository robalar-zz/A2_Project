from .atoms import Base, Atom
from .numbers import Number


class Expression(Base):

    def __init__(self, *args):
        super(Expression, self).__init__()

        self.args = [Number(x) if isinstance(x, (long, int, float)) else x for x in args]

    """def __new__(cls, *args):
        obj = Base.__new__(cls)
        obj.args = [Number(x) if isinstance(x, (long, int, float)) else x for x in args]   # Makes expression mutable, change?

        return obj"""


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

    """def __contains__(self, item):

        if item.__class__ == self.__class__ and _sublist(self.args, item.args):
            return True

        for sub_expr in self:
            if sub_expr == item:
                return True

            if isinstance(sub_expr, Expression) and item in sub_expr:
                return True"""

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, str(self.args)[1:-1])

    """def __iter__(self):
        return iter(self.args)"""

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.args == other.args
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


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
