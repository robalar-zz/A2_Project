from .expr import Expression, postorder

import copy

def subs(expression, old_term, new_term):

    # FIXME: Add type checking
    # TODO: Add multiple subs per call

    final_expression = copy.deepcopy(expression)

    if final_expression == old_term:
        final_expression = new_term

    for node in postorder(final_expression):
        if isinstance(node, Expression):
            for i, sub_expr in enumerate(node.args):
                if sub_expr == old_term:
                    node.args[i] = new_term

    return final_expression
