from decimal import Decimal
from fractions import Fraction
from .symbol import Symbol
from .numbers import Number
from .base import Base


def convert_type(arg):

    if isinstance(arg, Base):
        return arg
    if isinstance(arg, (int, long, float, Decimal, Fraction)):
        return Number(arg)
    if isinstance(arg, basestring):
        try:
            return Number(float(arg))
        except ValueError:
            return Symbol(arg)

    raise ValueError('Cannot convert type \'{}\' into internal equivalent'.format(type(arg)))

def convert_args(func):
    def func_wrapper(*args):
        new_args = [convert_type(x) for x in args]
        return func(*new_args)
    return func_wrapper