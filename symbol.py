__author__ = 'Rob'


class symbol(object):

    def __init__(self, name):
        self.name = name
        self.exponent = 1
        self.coeffiecent = 1

    def __add__(self, other):
        if self.name == other.name and self.exponent == other.exponent:
            self.coeffiecent += other.coeffiecent
            return self

    def __mul__(self, other):
        if type(other) is symbol and self.name == other.name:
            self.coeffiecent *= other.coeffiecent
            self.exponent += other.exponent
            return self
        elif type(other) is int or type(other) is float:
            self.coeffiecent *= other
            return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power, modulo=None):
        self.exponent += power
        return self

    def __str__(self):

        string = ''

        if self.coeffiecent != 1:
            string += str(self.coeffiecent)
        if self.coeffiecent != 0:
            string += self.name
        if self.exponent != 1:
            string += '^{}'.format(self.exponent)

        return string

x = symbol('x')

print 3*x


