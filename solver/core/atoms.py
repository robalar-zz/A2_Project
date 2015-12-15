class Atom(object):
    """ Base class for any atomic type
    """
    pass


class Number(Atom):
    pass


class Integer(Number):

    def __init__(self, value):
        self.value = value