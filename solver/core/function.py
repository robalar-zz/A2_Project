from .expr import Expression


class Function(Expression):

    name = None
    commutative = False
    nargs = 1

    @property
    def derivative(self):
        return None

    def __new__(cls, *args):
        if len(args) > cls.nargs:
            raise ValueError('Too many args passed to {}'.format(cls.name))
        elif len(args) < cls.nargs:
            raise ValueError('Not enough args passed to {}'.format(cls.name))


        return super(Function, cls).__new__(cls, *args)

    def __hash__(self):
        return hash(self.name)

    @property
    def basic_string(self):
        return '{}({})'.format(self.name, ''.join([x.basic_string for x in self.args]))

    @property
    def latex(self):
        return '\\{}({})'.format(self.name, ''.join([x.latex for x in self.args]))

    @classmethod
    def eval(cls, args):
        return self