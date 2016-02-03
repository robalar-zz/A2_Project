from nose.tools import assert_equal

from solver.core.expr import *


def test_expr_eq():

    expression1 = Expression(5,6)
    expression2 = Expression(5,6)

    assert_equal(expression1, expression2)


def test_contains():
    expression = Expression(1, 2, 3, Expression(4), 5, 6)
    assert 2 in expression
    assert 4 in expression
    assert Expression(1,2,3) in expression


def test_replace():

    expression = Expression(5,7)
    expression.replace(7,5)
    assert_equal(expression, Expression(5, 5))


def test_subexpressions():

    expression = Expression(1, 2, 3, Expression(4), Expression(5), 6)
    subexprs = subexpressions(expression)
    assert_equal(subexprs, [Expression(4), Expression(5)])


def test_postorder():
    expression = Expression(Expression(5, 4), Expression(3, 2), 1)
    po = list(postorder(expression))

    assert_equal(po, [5, 4, Expression(5, 4), 3, 2, Expression(3, 2), 1, Expression(Expression(5, 4), Expression(3, 2), 1)])