from operations import *

__author__ = 'Rob'


class Symbol(object):
    """ Represents an algebraic constant.

    An atomic algebraic component that can be used in expressions alongside numbers and other symbols.

    Attributes:
        name: A string identifier that is unique
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __add__(self, other):
        # TODO: Re-implement
        pass

    def __eq__(self, other):
        """
        >>> Symbol('x') == Symbol('x')
        True
        >>> Symbol('x') == Symbol('y')
        False
        >>> Symbol('x') == 9
        False
        """

        if isinstance(other, Symbol):
            return self.name == other.name

        return False

    def __ne__(self, other):
        return not self.__eq__(other)
