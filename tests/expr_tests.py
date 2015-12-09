from solver.core.expr import Expression
from solver.core.operations import *
from solver.core.symbol import Symbol
from solver.core.structs import Node

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises


def test_sanitise_unary():
    # -7 = -1 * 7
    assert_equal(Expression.sanitise_unary([UMin, 7]), [-1, Mul, 7])
    # 5 * -8 = 5 * -1 * 8
    assert_equal(Expression.sanitise_unary([5, Mul, UMin, 8]), [5, Mul, -1, Mul, 8])

def test_shunting_yard():
    # Numerical test: 5 + 3
    assert_equal(Expression._shunting_yard([5, Add, 3]), [5, 3, Add])
    # Symbol test: x * y
    x = Symbol('x')
    y = Symbol('y')
    assert_equal(Expression._shunting_yard([x, Mul, y]), [x, y, Mul])
    # Bracket test: (5 + 4) * 6
    assert_equal(Expression._shunting_yard(['(', 5, Add, 4, ')', Mul, 6]), [5, 4, Add, 6, Mul])
    # Extreme case: 3^6 *((x/7) / (y*10))
    assert_equal(Expression._shunting_yard([3, Pow, 6, Mul, '(', '(', x, Div, 7, ')', Div, '(', y, Mul, 10, ')', ')']),
                 [3, 6, Pow, x, 7, Div, y, 10, Mul, Div, Mul])
    # Mismatched parenthesis
    assert_raises(SyntaxError, Expression._shunting_yard, ['(', 4, Mul, 5, Add, 6])

def test_rpn_to_ast():
    # 5 3 +
    assert_equal(Expression._rpn_to_ast([5, 3, Add]), Node(Add, [Node(5), Node(3)]))
    # x y + 5 *
    x = Symbol('x')
    y = Symbol('y')
    assert_equal(Expression._rpn_to_ast([x, y, Add, 5, Mul]), Node(Mul, [Node(Add, [Node(x), Node(y)]), Node(5)]))