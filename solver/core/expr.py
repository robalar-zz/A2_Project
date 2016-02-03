from .atoms import Base


class Expression(Base):

    def __new__(cls, *args):
        obj = Base.__new__(cls)
        obj.args = list(args)  # Makes expression mutable, change?

        return obj

    def replace(self, old, new):
        self.args = [new if x == old else x for x in self.args]
        return self

    def __contains__(self, item):

        if item.__class__ == self.__class__ and _sublist(self.args, item.args):
            return True

        for sub_expr in self:
            if sub_expr == item:
                return True

            if isinstance(sub_expr, Expression) and item in sub_expr:
                return True

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, str(self.args)[1:-1])

    def __iter__(self):
        return iter(self.args)

    def __eq__(self, other):
        if self.__class__ == other.__class__ and self.args == other.args:
            return True
        else:
            return False


def subexpressions(expression, types=Expression):
    return [x for x in expression.args if isinstance(x, types)]


def _sublist(list, pattern):
    return [x for x in list if x in set(pattern)]


def postorder(node):

    if isinstance(node, Expression):
        for arg in node:
            for sub in postorder(arg):
                yield sub

    yield node

