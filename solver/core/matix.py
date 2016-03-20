from .function import Function
from .numbers import Infinity, Undefined, Number


class Matrix(Function):

    name = 'Matrix'
    nargs = Infinity()

    def __init__(self, *rows):
        super(Matrix, self).__init__(*rows)

        if not all(len(n) == len(rows[0]) for n in rows[1:]):
            raise ValueError('All row of a matrix must be the same length')

        self.m = len(rows)
        self.n = len(rows[0])

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

    # TODO: Make type conversion consistent
    def __mul__(self, other):
        if isinstance(other, Matrix):

            if self.n != other.m:
                return Undefined()

            final = []
            for i in range(1, self.m + 1):
                row = []
                for j in range(1, other.n + 1):
                    s = sum([self(i, k) * other(k, j) for k in range(1, self.n + 1)])
                    row.append(s)
                final.append(row)

            return Matrix(*final)

        else:
            flattened = sum(self.args, [])
            rows = [[flattened[i]*other for i in range(j + self.n)] for j in range(self.m)]
            return Matrix(*rows)

    def __div__(self, other):
        return self * Number(other)**-1

    def __pow__(self, power, modulo=None):
        if isinstance(power, Matrix):
            raise NotImplementedError
        else:
            flattened = sum(self.args, [])
            rows = [[flattened[i]**power for i in range(j + self.n)] for j in range(self.m)]
            return Matrix(*rows)

    def __add__(self, other):
        if isinstance(other, Matrix):
            if (self.m, self.n) != (other.m, other.n):
                return Undefined()

            final = []
            for i in range(1, self.m + 1):
                row = []
                for j in range(1, self.n + 1):
                    row.append(self(i, j) + other(i, j))
                final.append(row)

            return Matrix(*final)

        else:
            flattened = sum(self.args, [])
            rows = [[flattened[i] + other for i in range(j + self.n)] for j in range(self.m)]
            return Matrix(*rows)

    def __sub__(self, other):
        return self + Number(other) * -1

    def __iter__(self):
        return iter(sum(self.args, []))  # Flattens matrix


def linear_space(start, stop, n=50):
    def gen():
        if n == 1:
            yield stop
            return
        h = (stop - start) / (n - 1)
        for i in range(n):
            yield start + h*i

    l = list(gen())
    return Matrix(l)