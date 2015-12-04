class Operator(object):

    symbol = None
    precedence = None
    association = None
    commutative = False

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
    commutative = True

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
    commutative = True

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


def is_operator(token, op=Operator):
        try:
            if not issubclass(token, op):
                return False
            return True
        except TypeError:
            # token is not a class (or operator)
            return False


def is_commutative_operator(token):
    return is_operator(token) and token.commutative
