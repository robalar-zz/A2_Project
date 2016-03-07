from nose.tools import assert_equal

from solver.core.numbers import Integer, Undefined, Number
from solver.core.order import is_asae, isordered
from solver.core.symbol import Symbol
from solver.core.operations import Mul, Add, Pow
from solver.trigonometry.functions import sin, cos
from solver.calculus.differentate import d

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
    assert_equal(is_asae(Pow((x*y), Number(2))), False)
    assert_equal(is_asae(Pow(Number(1) + x, Number(1))), False)
    assert_equal(is_asae(Pow(Number(1), x)), False)


def is_ordered_test():
    # O-1
    assert_equal(isordered(Number(2), Number(3)), True)
    assert_equal(isordered(Number(1,2), Number(1)), True)
    assert_equal(isordered(Number(7,5), Number(1)), False)

    # O-2
    x = Symbol('x')
    y = Symbol('y')
    abc = Symbol('abc')
    bcd = Symbol('bcd')

    assert_equal(isordered(x, y), True)
    assert_equal(isordered(bcd, abc), False)

    # O-3
    assert_equal(isordered(Mul(y, x), Mul(Number(2), x, y)), True)
    assert_equal(isordered(Mul(Number(1), x,y), Mul(Number(2), x, y)), True)
    assert_equal(isordered(Mul(x, y), Mul(Number(6), x, y)), True)

    # O-4
    assert_equal(isordered(x**2, y**3), True)
    assert_equal(isordered(x**2, x**3), True)

    # O-6
    assert_equal(isordered(cos(x), sin(x)), True)
    assert_equal(isordered(sin(x), sin(y)), True)

    # O-7
    assert_equal(isordered(Number(2), x), True)

    # O-8
    a = Symbol('a')
    assert_equal(isordered(a*x**2, x**3), True)

    # O-9
    assert_equal(isordered((1+x)**3, (1+y)), True)

    # O-10
    assert_equal(isordered(1+x, y), True)

    # O-12
    s = Symbol('sin')  # why anyone would do this is beyond me, but worst case scenario...
    assert_equal(isordered(s, sin(x)), True)
    assert_equal(isordered(a, sin(x)), True)

    # O-13
    assert_equal(isordered(x, x**2), True)
