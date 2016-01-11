from tokenize import generate_tokens, untokenize
import token
from StringIO import StringIO
from keyword import iskeyword
import unicodedata

def tokenize(s):
    usr_inp = StringIO(s.strip())
    result = []
    for token_num, token_val, _, _, _ in generate_tokens(usr_inp.readline):
        result.append((token_num, token_val))

    return result

def is_function(token_str, local_dict, global_dict):
    func = local_dict.get(token_str)
    if func is None:
        func = global_dict.get(token_str)

    return callable(func) and not isinstance(func, Symbol)


def split_symbols(tokens, local_dict, global_dict):

    result = []

    for token_number, token_value in tokens:
        if token_number == token.NAME:
            try:
                unicodedata.lookup('GREEK SMALL LETTER ' + token_value)
                result.append((token_number, token_value))
            except KeyError:
                for char in token_value:
                    result.append((token.NAME, char))
        else:
            result.append((token_number, token_value))

    return result


def create_symbols(tokens, local_dict, global_dict):

    result = []
    previous_token = (None, None)

    tokens.append((None, None))

    for tok, next_tok in zip(tokens, tokens[1:]):

        tok_num, tok_value = tok
        next_tok_num, next_tok_value = next_tok

        if tok_num == token.NAME:

            # if the token is a keyword...
            if(tok_value in [None, True, False] or iskeyword(tok_value)
                # ...already initialized...
                or tok_value in local_dict
                # ...is an attribute access...
                or (previous_token[0] == token.OP and previous_token[1] == '.')
                # ...is a keyword argument...
                or (previous_token[0] == token.OP and previous_token[1] in ('(', ',')
                    and next_tok_num == token.OP and next_tok_value == '=')):

                result.append((token.NAME, tok_value))
                continue

            # Create the function call
            result.extend([
                (token.NAME, 'Symbol'),
                (token.OP, '('),
                (token.NAME, repr(tok_value)),
                (token.OP, ')')
            ])
        else:
            # If it isn't a NAME token leave it unchanged
            result.append((tok_num, tok_value))

        previous_token = tok

    return result


def create_numbers(tokens, local_dict, global_dict):

    result = []

    for token_number, token_value in tokens:
        if token_number == token.NUMBER:
            if '.' in token_value:
                pass
            else:
                result.extend([
                    (token.NAME, 'Integer'),
                    (token.OP, '('),
                    (token.NUMBER, token_value),
                    (token.OP, ')')
                ])
        else:
            result.append((token_number, token_value))

    return result


def implied_multiplication(tokens, local_dict, global_dict):

    result = []
    tokens.append((None, None))

    for tok, next_tok in zip(tokens, tokens[1:]):
        result.append(tok)
        # Left parenthesis next to right parenthesis
        if tok[0] == next_tok[0] == token.OP and tok[1] == ')' and next_tok[1] == '(':
            result.append((token.OP, '*'))
        if tok[0] == token.OP and tok[1] == ')' and next_tok[0] == token.NAME:
            result.append((token.OP, '*'))

    return result


transforms = [split_symbols, create_symbols, create_numbers, implied_multiplication]


def parse(s, local_dictionary=None, global_dictionary=None, transformations=transforms):

    if local_dictionary is None:
        local_dictionary = {}

    if global_dictionary is None:
        global_dictionary = {}  # FIXME: Temp fix
        global_dictionary = __import__('solver', global_dictionary, local_dictionary, ['*']).__dict__

    tokens = tokenize(s)

    for transform in transformations:
        tokens = transform(tokens, local_dictionary, global_dictionary)

    code = untokenize(tokens)
    compiled = compile(code, '<string>', 'eval')
    return eval(compiled, global_dictionary, local_dictionary)

c = parse('5*5*5')
print c
