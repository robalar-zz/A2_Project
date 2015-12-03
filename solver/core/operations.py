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

    def __init__(self, *args):
        pass


class Sub(Operator):

    symbol = '-'
    precedence = 2
    association = 'left'

    def __init__(self, left, right):
        pass


class UMin(Operator):

    symbol = '-u'
    precedence = 4
    association = 'right'
