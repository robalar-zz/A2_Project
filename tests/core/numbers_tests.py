from nose.tools import assert_equal
from nose.tools import assert_is_instance
from nose.tools import assert_not_equal, assert_false


from solver.core.numbers import *
from solver.core.symbol import Undefined


def number_test():
    assert_is_instance(Number(1), Atom)
    assert_is_instance(Number(56), Integer)
    assert_is_instance(Number(1, 4), Rational)
    assert_is_instance(Number('1.14125'), Rational)

    assert_equal(str(Number(1,3)), '1/3')


def number_arithmetic_test():
    assert_equal(Number(1) + Number(2), Number(3))
    assert_equal(Number(1,2) + Number(2), Number(5,2))
    assert_equal(Number(1,2) + Number(1,4), Number(3,4))

    assert_equal(Number(1) - Number(2), Number(-1))
    assert_equal(Number(2,5) - Number(1,5), Number(1,5))
    assert_equal(Number(1) - Number(1,3), Number(2,3))

    assert_equal(Number(5) * Number(3), Number(15))
    assert_equal(Number(1,2) * Number(6), Number(3))
    assert_equal(Number(4, 6) * Number(2, 4), Number(8, 24))

    assert_equal(Number(6)/Number(2), Number(3))
    assert_equal(Number(5)/Number(10), Number(1,2))
    assert_equal(Number(5)/Number(2,5), Number(25,2))
    assert_equal(Number(3,2)/Number(6,7), Number(7,4))
    assert_is_instance(Number(354)/Number(0), Undefined)

    assert_equal(Number(2)**Number(4),Number(16))
    # Fractional powers are not evaluated, even perfect roots, change?
    assert_equal(Number(27)**Number(1,3), Number(27)**Number(1,3))
    assert_equal(Number(1,3)**Number(-1), Number(3))
    assert_is_instance(Number(0)**Number(-1), Undefined)


def number_equality_test():
    assert_equal(Number(3), Number(3))
    assert_equal(Number(2,1), Number(2))
    assert_equal(Number(1,2), Number(2,4))

    assert_equal(Number(1) < Number(2), True)
    assert_equal(Number(1,3) < Number(1), True)
    assert_equal(Number(1,4) < Number(1,2), True)
    assert_equal(Number(1) < 45, True)

    assert_equal(Number(1) > Number(2), False)
    assert_equal(Number(1,3) > Number(1), False)
    assert_equal(Number(1,4) > Number(1,2), False)
    assert_equal(Number(3,5) > 4, False)

    assert_false(Number(0) < Number(0))
    assert_false(Number(0) > Number(0))


def undefined_test():
    assert_not_equal(Undefined(), Undefined())
    assert_not_equal(Number(2)/Number(0), Undefined())
    assert_is_instance(Undefined() + 1, Undefined)
    assert_is_instance(Undefined() - 1, Undefined)
    assert_is_instance(Undefined() * 4, Undefined)
    assert_is_instance(Undefined() / 6, Undefined)
