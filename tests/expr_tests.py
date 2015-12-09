from solver.core.expr import Expression
from solver.core.operations import *

from nose.tools import assert_equal
from nose.tools import assert_not_equal


def test_sanitise_unary():
    # -7 = -1 * 7
    assert_equal(Expression.sanitise_unary([UMin, 7]), [-1, Mul, 7])
    # 5 * -8 = 5 * -1 * 8
    assert_equal(Expression.sanitise_unary([5, Mul, UMin, 8]), [5, Mul, -1, Mul, 8])

def test_shunting_yard():
