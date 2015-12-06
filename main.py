from solver.core.expr import *
from solver.core.structs import *
from solver.core.symbol import Symbol

a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')
e = Symbol('e')
f = Symbol('f')
x = Symbol('x')
y = Symbol('y')

e = Expression([x, Pow, a, Mul, y, Pow, b, Mul, x, Pow, c, Add, e])
for n in e.ast:
    print n.value