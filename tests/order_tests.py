from nose.tools import assert_equal

from solver.core.numbers import Integer, Undefined, Number
from solver.core.order import is_asae
from solver.core.symbol import Symbol
from solver.core.operations import Mul, Add, Pow

def asae_1_test():
    assert_equal(is_asae(Integer(2)), True)

def asae_3_test():
    assert_equal(is_asae(Symbol('x')), True)
    assert_equal(is_asae(Undefined), False)

def asae_4_test():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    assert_equal(is_asae(Mul(Number(2), x, y, z**Number(2))), True)
    assert_equal(is_asae(Mul(Number(2), Mul(x, y), z**Number(2))), False)
    assert_equal(is_asae(Mul(Number(1), x, y, z**Number(2))), False)
    assert_equal(is_asae(Mul(Number(2), x, y, z, z**Number(2))), False)
    assert_equal(is_asae(Mul(Number(2), Number(3), z, x, y)), False)
    assert_equal(is_asae(Mul(z, y, x)), False)

def asae_5_test():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    assert_equal(is_asae(Add(Number(2) * x, Number(3) * y, Number(4) * z)), True)
    assert_equal(is_asae(Add(Number(1), Add(x, y), z)), False)
    assert_equal(is_asae(Add(Number(1), Number(2), x)), False)
    assert_equal(is_asae(Add(Number(1), x, Mul(Number(2), x))), False)
    assert_equal(is_asae(Add(z, y, x)), False)

def asae_6_test():
    x = Symbol('x')
    y = Symbol('y')

    assert_equal(is_asae(x**Number(2)), True)
    assert_equal(is_asae((Number(1) + x)**Number(3)), True)
    assert_equal(is_asae(Number(2)**x), True)
    assert_equal(is_asae(Pow(Number(2), Number(3))), False)
    assert_equal(is_asae((x**Number(2))**Number(3)), False)
    assert_equal(is_asae((x*y)**Number(2)), False)
    assert_equal(is_asae((Number(1) + x)**Number(1)), False)
    assert_equal(is_asae(Number(1)**x), False)