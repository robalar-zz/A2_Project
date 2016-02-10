from .operations import *
from .expr import postorder
from subs import subs
from expr import subexpressions

from itertools import groupby
import copy


# TODO: Use subs?

def to_power_of_zero(expression):
    for symbol in expression.atoms():
        expression = subs(expression, symbol**Number(0), Number(0))
    return expression


def to_the_power_of_one(expression):
    for symbol in expression.atoms():
        expression = subs(expression, symbol**Number(1), symbol)
    return expression


def multiplied_by_zero(expression):
    for symbol in expression.atoms():
        expression = subs(expression, symbol*Number(0), Number(0))
    return expression


def multiplied_by_one(expression):
    for symbol in expression.atoms():
        expression = subs(expression, symbol*Number(1), symbol)
    return expression


def add_zero(expression):
    for symbol in expression.atoms():
        expression = subs(expression, symbol + Number(0), symbol)
    return expression


def combine_powers(expression):
    for subexpr in postorder(expression):
        if isinstance(subexpr, Mul):
            for symbol in subexpressions(subexpr, Symbol):  # x -> x^1
                subexpr.replace(symbol, symbol**Number(1))

            powers = subexpressions(subexpr, Pow)  # Get all power sub-expressions
            powers = sorted(powers, key=lambda x: x.base)  # [Pow(x,2), Pow(y,2), Pow(x, 9)] -> [Pow(x,2), Pow(x, 9), Pow(y,2)]
            # List of lists of Pows with identical bases
            like_bases = [list(group) for key, group in groupby(powers, key=lambda x: x.base)]

            for item in like_bases:
                final_pow = item[0].base ** Add(*[sub.exponent for sub in item])  # Create the new Pow expression
                old_expr = Mul(*item)  # Get the item to replace
                expression = subs(expression, old_expr, final_pow)  # replace the expression

    return expression

# WHAT THE HELL?
def add_symbols(expression):
    for subexpr in postorder(expression):
        if isinstance(subexpr, Add):
            for symbol in subexpressions(subexpr, Symbol):  # x -> x * 1
                subexpr.replace(symbol, symbol * Number(1))

            for sub_expr in subexpressions(subexpr, Mul):  # x*y -> 1*x*y
                if not subexpressions(sub_expr, Number):
                    sub_expr.args.append(Number(1))

            muls = subexpressions(subexpr, Mul)

            for m in muls:
                if not subexpressions(m, Symbol):
                    muls.remove(m)

            muls = sorted(muls, key=lambda x: subexpressions(x, Symbol))
            same_symbol = [list(group) for key, group in groupby(muls, key=lambda x: subexpressions(x, Symbol))]
            for group in same_symbol:
                coeff = Add(*[Add(*subexpressions(x, Number)) for x in group])
                symbols = subexpressions(group[0], Symbol)
                final_term = Mul(coeff, *symbols)  # Does it work for multi-symbols?
                final_term = remove_one_item_exprs(final_term)
                old_term = Add(*group)
                old_term = fold_nested(old_term)
                expression = subs(expression, old_term, final_term)

    return expression


def fold_nested(expression):
    for sub in postorder(expression):
        for sub_expression in subexpressions(sub, sub.__class__):
            sub.args.extend(sub_expression.args)
            sub.args.remove(sub_expression)

    return expression


def remove_one_item_exprs(expression):
    for subexpr in postorder(expression):
        if isinstance(subexpr, Expression) and len(subexpr.args) == 1:
            expression = subs(expression, subexpr, subexpr.args[0])

    return expression


def fold_constants(expression):
    for subexpr in postorder(expression):
        if isinstance(subexpr, Expression) and subexpressions(subexpr, Number):
            numbers = subexpressions(subexpr, Number)
            print numbers
            final = expression.eval()
            print final
    return expression

simplifications = [to_the_power_of_one, to_power_of_zero, add_zero, multiplied_by_one, multiplied_by_zero]

simplifications = [fold_nested, combine_powers, to_the_power_of_one, to_power_of_zero, add_symbols, multiplied_by_zero,
                   multiplied_by_one, add_zero, remove_one_item_exprs, fold_constants]


def simplify(expression, simplification_list=simplifications):

    old_form = None

    while old_form != expression:

        old_form = copy.deepcopy(expression)
        for simplification in simplification_list:
            expression = simplification(expression)

    return expression


def _simplify(expression, simplification_list):
    for simplification in simplification_list:
        for subexpression in postorder(expression):
            if isinstance(subexpression, Expression):
                simplified_sub = simplification(subexpression)
                normal_form = subs(expression, subexpression, simplified_sub)

    return normal_form