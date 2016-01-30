from .atoms import Base


class Expression(Base):

    def __new__(cls, *args):
        obj = Base.__new__(cls)
        obj.args = list(args)

        return obj

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, str(self.args)[1:-1])

    def __iter__(self):
        return iter(self.args)


def is_redex(obj):
    return hasattr(obj, 'args')
