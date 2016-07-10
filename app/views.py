from flask import render_template, request
from app import app

from solver.core import *
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

    return modules


def get_graph(function):

    v = variables(function)

    if len(v) == 1:
        return render_template('graph.html', title='Graph', function= basic_console(function), type='linear')
    elif len(v) == 2:
        return render_template('graph.html', title='Graph', function=basic_console(function), type='implicit')



@app.route('/input', methods=['GET'])
def input():

    i = request.args.get('i')

    return render_template('index.html', modules=get_modules(i))


def translate_latex(latex_string):

    nodelist, tpos, tlen = latexwalker.get_latex_nodes(latex_string, keep_inline_math=False, tolerant_parsing=False)

    default_macro_dict['frac'] = MacroDef('frac', '(%s)/(%s)')
    default_macro_dict['cdot'] = MacroDef('cdot', '*')

    return LatexNodes2Text(macro_dict=default_macro_dict).nodelist_to_text(nodelist)
