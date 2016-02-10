from nose.tools import assert_equal

from solver.core.atoms import *
from solver.core.operations import *
# TODO: REWRITE
"""
def test_base():
    base1 = Base()
    base2 = Base()

    # Adding
    added = base1 + base2
    assert_equal(added, Add(base1, base2))

    radded = 1 + base1
    assert_equal(radded, Add(base1, 1))

    # Misusing
    minuses = base1 - base2
    assert_equal(minuses, Add(base1, Mul(-1, base2)))

    rsub = 1 - base1
    assert_equal(rsub, Add(base1, Mul(-1, 1)))

    # Unary operations
    assert_equal(-base1, Mul(base1, -1))
    assert_equal(+base1, base1)

    # Exponentiation
    power = base1 ** base2
    assert_equal(power, Pow(base1, base2))

    # Dividing
    dividing = base1 / base2
    assert_equal(dividing, Mul(base1, Pow(base2, -1)))

def test_atom():
    a = Atom()
    assert isinstance(a, (Base, Atom))"""



