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



v = (Number(1)/(Number(1)/a + c/(a*b)) + ((a*b*c) + a*c**Number(2))/(b+c)**Number(2) - a)

print repr(rational_expand(v))