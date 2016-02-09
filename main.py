from solver import *
a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')
e = Symbol('e')
f = Symbol('f')
x = Symbol('x')
y = Symbol('y')

# FIXME
expr = Number(7)*x + Number(10)*x - Number(2) * x
print simplify(expr)
