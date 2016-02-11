#from __future__ import print_function

from .expr import Expression

import copy

# OLD VERSION
def subs(expression, old_term, new_term):

    # TODO: Add rearrangement of old term
    # TODO: Add multiple subs per call

    final_expression = copy.deepcopy(expression)

    if old_term == new_term:
        return final_expression

    if final_expression == old_term:
        final_expression = new_term

    if isinstance(final_expression, Expression):
        args = final_expression.args
        #print('expr:{}'.format(final_expression))
        #print('args len:{}'.format(len(args)))
        #print('args:{}'.format(args))
        for i, arg in enumerate(args):
            arg = subs(arg, old_term, new_term)
            if not arg == args[i]:
                args[i] = arg

        final_expression.args = args

    return final_expression

# NEW SHINY VERSION
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