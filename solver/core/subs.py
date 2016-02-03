from .expr import Expression, postorder

import copy

def subs(expression, old_term, new_term):

    # TODO: Add rearrangement of old term
    # TODO: Add multiple subs per call

    final_expression = copy.deepcopy(expression)

    if old_term == new_term:
        return final_expression

    if final_expression == old_term:
        final_expression = new_term

    for node in postorder(final_expression):
        if isinstance(node, Expression):
            node.replace(old_term, new_term)

    return final_expression
