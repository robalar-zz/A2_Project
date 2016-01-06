from symbol import Symbol

from tokenize import generate_tokens
import token
from StringIO import StringIO
from keyword import iskeyword


def tokenize(s):

    result = []
    for token_num, token_val, _, _, _ in generate_tokens(StringIO(s).readline):
        result.append((token_num, token_val))

    return result

def is_function(token_str, local_dict, global_dict):
    func = local_dict.get(token_str)
    if func is None:
        func = global_dict.get(token_str)

    return callable(func) and not isinstance(func, Symbol)


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
                (token.NAME, tok_value),
                (token.OP, ')')
            ])
        else:
            # If it isn't a NAME token leave it unchanged
            result.append((tok_num, tok_value))

        previous_token = tok

    return result


