from solver import *

a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')
e = Symbol('e')
f = Symbol('f')
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

#TODO: implment functions, and factorials (F'n hell) ;)
#TODO: Finish implementing evaluate.py

# FIXME
#expr = Number(7)*x + Number(10)*x - Number(2) * x
#print simplify(expr)

from solver.core.simplify import *

print auto_simplify(Number(4)*(Number(2)**Number(-1)))