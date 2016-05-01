from decimal import Decimal
from fractions import Fraction


def convert_type(arg):
    from .numbers import Number
    from .symbol import Symbol
    from .base import Base

    if isinstance(arg, Base):
        return arg
    if isinstance(arg, (int, long, float, Decimal, Fraction)):
        return Number(arg)
    if isinstance(arg, basestring):
        try:
            return Number(float(arg))
        except ValueError:
            return Symbol(arg)

    raise ValueError('Cannot convert {} of type \'{}\' into internal equivalent'.format(arg, type(arg)))


def convert_args(func):
    def func_wrapper(*args):
        new_args = [convert_type(x) for x in args]
        return func(*new_args)
    return func_wrapper


def convert_method_args(*args):

    def decorate(cls):
        for method in args:
            if callable(getattr(cls, method)):
                setattr(cls, method, convert_args(getattr(cls, method)))
        return cls
    return decorate
