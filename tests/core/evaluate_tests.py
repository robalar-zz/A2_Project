from nose.tools import assert_equal
from nose.tools import assert_raises

from solver.core.numbers import Number, Undefined
from solver.core.evaluate import *


def evalulate_add_test():
    assert_raises(ValueError, evaluate_add, 3, 4)
    assert_equal(evaluate_add(Number(4), Number(6)), Number(10))
    assert_equal(evaluate_add(Number(1,2), Number(1)), Number(3,2))
    assert_equal(evaluate_add(Number(3,2), Number(1,6)), Number(5,3))


def evaluate_mul_test():
    assert_raises(ValueError, evaluate_mul, 5, 3)
    assert_equal(evaluate_mul(Number(5), Number(2)), Number(10))
    assert_equal(evaluate_mul(Number(1,5), Number(2)), Number(2,5))
    assert_equal(evaluate_mul(Number(3,4), Number(1,2)), Number(3,8))


def evaluate_power_test():
    assert_raises(ValueError, evaluate_power, Number(4), Number(1,2))
    assert_raises(ValueError, evaluate_power, 5, Number(2))
    assert_equal(evaluate_power(Number(5,8), Number(-2)), Number(64, 25))
    assert_equal(evaluate_power(Number(0), Number(435)), Number(0))
    assert_equal(isinstance(evaluate_power(Number(0), Number(0)), Undefined), True)
    assert_equal(isinstance(evaluate_power(Number(0), Number(-5)), Undefined), True)