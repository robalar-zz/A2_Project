from flask import render_template, request
from app import app

from solver import *
from solver.polynomials.general_polynomial import variables
from solver.formating import latex, basic_console
from pylatexenc import latexwalker
from pylatexenc.latex2text import default_macro_dict, LatexNodes2Text, MacroDef


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


def get_modules(user_input):

    modules = []

    modules.append(render_template('input.html', title='Input', input=user_input))

    # Parse into solver
    parsed = parse(translate_latex(user_input))

    # format parsed input to latex and add to modules
    formatted = latex.latex(parsed)
    modules.append(render_template('input.html', title='Result', input=formatted))

    #graph test
    graph_module = get_graph(parsed)
    if graph_module:
        modules.append(graph_module)

    diff_module = get_diff(parsed)
    if diff_module:
        modules.append(diff_module)

    return modules


def get_graph(function):

    fn_string = ''
    fn_type = ''
    x_label = ''

    # do paremetics, implement eq finally?
    if isinstance(function, list):
        if len(function) == 2 and variables(function[0]) == variables(function[1]):
            data = ''

    elif isinstance(function, Eq):
        fn_string = (function.lhs - function.rhs).basic_string
        fn_type = 'implicit'

    else:
        v = variables(function)

        if len(v) == 1:
            fn_string = function.basic_string
            fn_type='linear'
            x_label = str(v.pop())

        elif len(v) == 2:
            fn_string = function.basic_string
            fn_type ='implicit'

    return render_template('graph.html', title='Graph', function=fn_string, type=fn_type, x_label=x_label)


def get_diff(function):

    derivatives = dict()

    vars = variables(function)
    for var in vars:
        d = derivative(function, var)
        derivatives[var] = d

    return render_template('diff.html', title='Derivatives', derivatives=derivatives, function=function)

@app.route('/input', methods=['GET'])
def input():

    i = request.args.get('i')

    return render_template('index.html', modules=get_modules(i))


def translate_latex(latex_string):

    nodelist, tpos, tlen = latexwalker.get_latex_nodes(latex_string, keep_inline_math=False, tolerant_parsing=False)

    default_macro_dict['frac'] = MacroDef('frac', '(%s)/(%s)')
    default_macro_dict['cdot'] = MacroDef('cdot', '*')

    return LatexNodes2Text(macro_dict=default_macro_dict).nodelist_to_text(nodelist)
