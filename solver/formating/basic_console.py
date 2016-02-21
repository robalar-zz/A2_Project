from ..core.operations import Add, Mul, Pow
from ..core.numbers import Number
from ..core.symbol import Symbol

from itertools import izip

# FIXME: COMPLETELY BROKEN

def infix(expression):

    def visit(node, prior_precedence):
        if isinstance(node, (Number, Symbol)):
            return str(node)
        # FIXME: for functions
        result = visit(node.args[0], node.precedence) + str(node) + visit(node.args[1], node.precedence)

        if node.precedence < prior_precedence:
            result = '(' + result + ')'

        return result

    e = to_binary(expression)
    return visit(e, e.precedence)


def to_binary(expression):
    if len(expression.args) <= 2:
        return expression
    else:
        a = iter(expression.args)
        couples = izip(a, a)
        expression.args = [] if len(expression.args) % 2 == 0 else [expression.args[-1]]
        for couple in couples:
            expression.args.append(expression.__class__(*couple))

    return expression
