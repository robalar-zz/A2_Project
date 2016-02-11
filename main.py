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

# FIXME
#expr = Number(7)*x + Number(10)*x - Number(2) * x
#print simplify(expr)

from solver.core.evaluate import evaluate_power

print evaluate_power(Number(0), Number(6))