from nose.tools import assert_equal
from nose.tools import assert_is_instance

from solver.core.operations import *
from solver.core.symbol import Symbol
from solver.trigonometry.functions import sin


def base_test():
    x = Symbol('x')

    assert_equal(base(x), x)
    assert_equal(base(x*5), x*5)
    assert_equal(base(x+2), x+2)
    assert_equal(base(sin(x)), sin(x))

    assert_equal(base(x**3), x)
    assert_equal(base(sin(x)**5), sin(x))
    assert_equal(base(Number(1,2)**Number(1,3)), Number(1,2))

    assert_is_instance(base(Number(2)), Undefined)
    assert_is_instance(base(Number(4,5)), Undefined)


def exponent_test():
    x = Symbol('x')

    assert_equal(exponent(x), Number(1))
    assert_equal(exponent(x*5),Number(1))
    assert_equal(exponent(x+2), Number(1))
    assert_equal(exponent(sin(x)), Number(1))

    assert_equal(exponent(x**3), Number(3))
    assert_equal(exponent(sin(x)**5), Number(5))
    assert_equal(exponent(Number(1,2)**Number(1,3)), Number(1,3))

    assert_is_instance(exponent(Number(2)), Undefined)
    assert_is_instance(exponent(Number(4,5)), Undefined)

# TODO: Finish these tests
def term_test():
    pass