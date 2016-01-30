from solver import *
a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')
e = Symbol('e')
f = Symbol('f')
x = Symbol('x')
y = Symbol('y')

expr = ((y + x) * y) ** y
print subs(expr, y, x)
