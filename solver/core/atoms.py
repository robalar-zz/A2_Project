class Atom(object):
    """ Base class for any atomic type
    """
    pass


class Number(Atom):
    pass


class Integer(Number):

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value + other.value)

    def __iadd__(self, other):
        return self + other

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):

        if isinstance(other, Integer):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)