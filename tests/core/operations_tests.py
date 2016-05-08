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


def term_test():
    x = Symbol('x')
    y = Symbol('y')

    assert_equal(term(x), Mul(x))
    assert_equal(term(x+5), Mul(x+5))
    assert_equal(term(x**5), Mul(x**5))
    assert_equal(term(sin(x)), Mul(sin(x)))

    assert_equal(term(6*x*3), Mul(x))
    assert_equal(term(10*x*y), x*y)

    assert_equal(term(x*y), x*y)

    assert_is_instance(term(Number(1)), Undefined)
    assert_is_instance(term(Number(3,4)), Undefined)


def const_test():
    x = Symbol('x')
    y = Symbol('y')

    assert_equal(const(x), Number(1))
    assert_equal(const(1+x), Number(1))
    assert_equal(const(y+x), Number(1))
    assert_equal(const(x**3), Number(1))
    assert_equal(const(sin(x)), Number(1))

    assert_equal(const(6*x*3), Number(18))
    assert_equal(const(10*x*y), Number(10))

    assert_equal(const(x*y), Number(1))

    assert_is_instance(const(Number(7)), Undefined)
    assert_is_instance(const(Number(1,4)), Undefined)
