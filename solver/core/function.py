from .expr import Expression


class Function(Expression):

    name = None

    nargs = 1

    def __init__(self, *args):
        super(Function, self).__init__()

        if len(args) > self.nargs:
            raise ValueError('Too many args passed to {}'.format(self.name))

        self.args = list(args)
