class Operator(object):

    symbol = None
    precedence = None
    association = None


class Pow(Operator):

    symbol = '**'
    precedence = 4
    association = 'right'

    def __init__(self, left, right):
        pass


class Mul(Operator):

    symbol = '*'
    precedence = 3
    association = 'left'

    def __init__(self, left, right):
        pass

    def __repr__(self):
        return self.symbol


class Div(Operator):

    symbol = '/'
    precedence = 3
    association = 'left'

    def __init__(self, left, right):
        pass


class Add(Operator):

    symbol = '+'
    precedence = 2
    association = 'left'

    def __init__(self, left, right):
        pass


class Sub(Operator):

    symbol = '-'
    precedence = 2
    association = 'left'

    def __init__(self, left, right):
        pass
