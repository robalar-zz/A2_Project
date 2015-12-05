from solver.core.expr import *
from solver.core.structs import *
from solver.core.symbol import Symbol

a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')
e = Symbol('e')
f = Symbol('f')

t = ASTNode(Mul, [ASTNode(a), ASTNode(Div, [ASTNode(b), ASTNode(c)]), ASTNode(Div, [ASTNode(d), ASTNode(e)]), ASTNode(f)])
ast = Expression.simplify_ast(t)
for n in ast:
    print n.value