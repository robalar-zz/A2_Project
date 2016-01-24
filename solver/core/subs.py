def subs(expression, old_term, new_term):

    #FIXME: Add type checking
    #TODO: Add multiple subs per call

    final_expression = expression

    for i, sub_expression in enumerate(final_expression):
        if sub_expression == old_term:
            final_expression.args[i] = new_term

    return final_expression
