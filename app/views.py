from flask import render_template, request
from app import app

from solver.core import *
from solver.formating import latex
from pylatexenc import latexwalker
from pylatexenc.latex2text import default_macro_dict, LatexNodes2Text, MacroDef


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


def get_modules(user_input):

    modules = []

    # Parse into solver
    parsed = parse(translate_latex(user_input))

    # format parsed input to latex and add to modules
    formatted = latex.latex(parsed)
    modules.append(render_template('input.html', title='Input', input=formatted))

    #graph test
    modules.append(render_template('graph.html', title='Graph'))

    return modules

@app.route('/input', methods=['GET'])
def input():

    i = request.args.get('i')

    return render_template('index.html', modules=get_modules(i))


def translate_latex(latex_string):

    nodelist, tpos, tlen = latexwalker.get_latex_nodes(latex_string, keep_inline_math=False, tolerant_parsing=False)

    default_macro_dict['frac'] = MacroDef('frac', '(%s)/(%s)')
    default_macro_dict['cdot'] = MacroDef('cdot', '*')

    return LatexNodes2Text(macro_dict=default_macro_dict).nodelist_to_text(nodelist)
