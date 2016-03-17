from .expr import Expression
from .symbol import Symbol
from .function import Function
from .numbers import Infinity, Undefined

class Matrix(Function):

    name = 'Matrix'
    nargs = Infinity()

    def __init__(self, *rows):
        super(Matrix, self).__init__(*rows)

        if not all(len(n) == len(rows[0]) for n in rows[1:]):
            raise ValueError('All row of a matrix must be the same length')

        self.n = len(rows)
        self.m = len(rows[0])


    def __call__(self, *args, **kwargs):

        if len(args) == 2 and all(isinstance(x, int) for x in args):
            i = args[0] - 1
            j = args[1] - 1
            try:
                return self.args[i][j]
            except IndexError:
                raise IndexError('Index ({}, {}) is out of range'.format(args[0], args[1]))

        elif len(kwargs) == 2:
            try:
                i = kwargs['i']
                j = kwargs['j']
            except KeyError:
                raise ValueError('Incorrect args passed to Matrix, use Matric(i=m, j=n)')

            return self(i, j)

        elif len(kwargs) == 1:
            if 'i' in kwargs:
                i = kwargs['i'] - 1
                return self.args[i]
            elif 'j' in kwargs:
                j = kwargs['j']
                return [self(i, j) for i in range(1, len(self.args)+1)]

        raise ValueError('Unknown call Matrix({}, {})'.format(args, kwargs))

    def __mul__(self, other):
        if isinstance(other, Matrix):

            if self.m != other.n:
                return Undefined()

            final = []
            for i in range(1, self.n + 1):
                row = []
                for j in range(1, other.m + 1):
                    s = sum([self(i, k) * other(k, j) for k in range(1, self.m + 1)])
                    row.append(s)
                final.append(row)

            return Matrix(*final)

        else:
            return super(Matrix, self).__mul__(other)


def dot_product(u, v):
    if len(u) != len(v):
        return Undefined()

    final = []

    for i, item in enumerate(u):
        final.append(item * v[i])

    return sum(final)