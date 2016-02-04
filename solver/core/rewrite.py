from .operations import *
from .expr import postorder
from subs import subs
from expr import subexpressions

from itertools import groupby
import copy


# TODO: Use subs?

def to_power_of_zero(expression):
    if isinstance(expression, Pow) and expression.exponent == Number(0):
        return Number(1)
    else:
        return expression


def to_the_power_of_one(expression):
    if isinstance(expression, Pow) and expression.exponent == Number(1):
        return expression.base
    else:
        return expression


def multiplied_by_zero(expression):
    if isinstance(expression, Mul) and Number(0) in expression.args:
        return Number(0)
    else:
        return expression


def multiplied_by_one(expression):
    if isinstance(expression, Mul) and Number(1) in expression.args:
        expression.args = [x for x in expression.args if x != Number(1)]

    return expression


def add_zero(expression):
    if isinstance(expression, Add) and Number(0) in expression.args:
        expression.args = [x for x in expression.args if x != Number(0)]
    return expression


def combine_powers(expression):
    if isinstance(expression, Mul):
        for symbol in subexpressions(expression, Symbol):  # x -> x^1
            expression.replace(symbol, symbol**Number(1))

        powers = subexpressions(expression, Pow)  # Get all power sub-expressions
        powers = sorted(powers, key=lambda x: x.base)  # [Pow(x,2), Pow(y,2), Pow(x, 9)] -> [Pow(x,2), Pow(x, 9), Pow(y,2)]

        like_bases = [list(group) for key, group in groupby(powers, key=lambda x: x.base)]  # List of lists of Pows with identical bases
        for item in like_bases:
            final_pow = item[0].base ** sum([sub.exponent for sub in item], Number(0))  # Create the new Pow expression
            old_expr = reduce(mul, item)  # Get the item to replace
            expression.replace(old_expr, final_pow)  # replace the expression

    return simplify(expression, [to_the_power_of_one])


def add_symbols(expression):
    if isinstance(expression, Add):
        for symbol in subexpressions(expression, Symbol):  # x -> x * 1
            expression.replace(symbol, symbol * Number(1))

        for sub_expr in subexpressions(expression, Mul):  # x*y -> 1*x*y
            if not sub_expr.atoms(Number):
                sub_expr.args.append(Number(1))

        muls = subexpressions(expression, Mul)
        muls = sorted(muls, key=lambda x: x.atoms(Symbol))
        same_symbol = [list(group) for key, group in groupby(muls, key=lambda x: x.atoms(Symbol))]
        for group in same_symbol:
            coeff = sum([sum(x.atoms(Number), Number(0)) for x in group], Number(0))
            final_term = reduce(mul, group[0].atoms(Symbol)) * coeff
            old_term = reduce(mul, group)
            expression.replace(old_term, final_term)

    return expression

def fold_nested(expression):
    for sub_expression in subexpressions(expression, expression.__class__):
        expression.args.extend(sub_expression.args)
        expression.args.remove(sub_expression)

    return expression


def remove_one_item_exprs(expression):
    if isinstance(expression, Expression) and len(expression.args) == 1:
        return expression.args[0]
    else:
        return expression

simplifications = [fold_nested, add_symbols, combine_powers, to_the_power_of_one, to_power_of_zero, multiplied_by_zero,
                   multiplied_by_one, add_zero, remove_one_item_exprs]


def simplify(expression, simplification_list=simplifications):

    normal_form = copy.deepcopy(expression)
    old_form = None

    while old_form != normal_form:

        old_form = copy.deepcopy(normal_form)

        for simplification in simplification_list:
            for subexpression in postorder(normal_form):
                simplified_sub = simplification(copy.deepcopy(subexpression))
                normal_form = subs(normal_form, subexpression, simplified_sub)
        print old_form, normal_form

    return normal_form
