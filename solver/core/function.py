from .expr import Expression

class Function(Expression):
    def __init__(self, name):
        super(Function, self).__init__()
        self.name = name

    def __repr__(self):
        return '{}({})'.format(self.name, str(self.args)[1:-1])