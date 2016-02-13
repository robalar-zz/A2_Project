from .expr import Expression


def _map(func, expression, *func_args):
    op = expression.__class__
    new_args = [func(x, *func_args) for x in expression.args]
    return op(*new_args)


def substitute(u, old, new):
    if isinstance(u, Expression):
        v = _map(substitute, u, old, new)
    else:
        v = u

    if v == old:
        return new
    else:
        return v