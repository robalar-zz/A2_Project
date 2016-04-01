from .numbers import Infinity, Undefined, Number
from .base import Base


class Matrix(Number):

    name = 'Matrix'
    nargs = Infinity()

    def __init__(self, *rows):
        
        super(Matrix, self).__init__()
        self.value = _Matrix(rows)

        if not all(len(n) == len(rows[0]) for n in rows[1:]):
            raise ValueError('All row of a matrix must be the same length')

    @property
    def m(self):
        return self.value.m

    @property
    def n(self):
        return self.value.n

    def __call__(self, i, j):
        return self.value.array[i][j]

    def __mul__(self, other):
        """if isinstance(other, Matrix):

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
            return Matrix(*rows)"""

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


class _Matrix(Base):

    def __init__(self, rows):
        self.array = list(rows)

        self.m = len(rows)
        self.n = len(rows[0])

    def __mul__(self, other):
        if isinstance(other, Matrix):

            if self.n != other.m:
                return Undefined()

            final = []
            for i in range(self.m):
                row = []
                for j in range(other.n):
                    s = sum([self.array[i][k] * other(k, j) for k in range(self.n)])
                    row.append(s)
                final.append(row)

            return Matrix(*final)

        else:
            flattened = sum(self.array, [])
            rows = [[flattened[i]*other for i in range(j + self.n)] for j in range(self.m)]
            return Matrix(*rows)

    def __str__(self):
        return str(self.array)

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