def rewrite(expression, rewrite_rules):

    normalised_expression = expression

    for rule in rewrite_rules:
         normalised_expression = rule(normalised_expression)

    return normalised_expression



