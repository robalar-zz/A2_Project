from solver import *

a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')
e = Symbol('e')
f = Symbol('f')
n = Symbol('n')
x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

from solver.polynomials.general_polynomial import expand

v = ((1/((x+y)**2+1))**Number(1,2))*((1/((x+y)**2+1))**Number(1,2)-1)/(x+1)
print v