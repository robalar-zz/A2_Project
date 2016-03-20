from .basic_console import basic_console


def ascii_math(u):

    string = basic_console(u)

    html = '''

    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
    .MathJax {
    font-size: 6em !important;
    }
    </style>

    <script type="text/javascript" src="mathjax/MathJax.js?config=AM_HTMLorMML-full"></script>

    </head>
    <body style="background-color:#f0f0f0">

    `%s`

    </body>
    </html>
    ''' % string

    return html