from ..core.operations import Add, Mul, Pow

from itertools import izip


def infix(expression):

    s = ''

    if isinstance(expression, (Add, Mul, Pow)):
        expression = to_binary(expression)
        s += '('
        s += infix(expression.args[0])

    s += str(expression)

    if isinstance(expression, (Add, Mul, Pow)):
        s += infix(expression.args[1])
        s += ')'

    return s

def to_binary(expression):
    if len(expression.args) <= 2:
        return expression
    else:
        if len(expression.args) % 2 != 0:
            expression.args.append(None)
        a = iter(expression.args)
        couples = izip(a, a)
        expression.args = []
        for couple in couples:
            if None not in couple:
                expression.args.append(expression.__class__(*couple))
            else:
                expression.args.append(expression.__class__(couple[0]))

    return expression
