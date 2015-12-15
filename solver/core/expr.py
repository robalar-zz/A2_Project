from collections import deque
from copy import deepcopy

from structs import Node, combine_children, in_children, instance_in_children
from symbol import Symbol, is_operator, is_commutative_operator
from operations import *

__author__ = 'Robert Hales'


class Expression(object):

    # Static methods

    @staticmethod
    def sanitise_unary(tokens):
        """ Replace unary minus tokens with -1, * in input token list

            Args:
                tokens: list of tokens to be sanitised

            Returns:
                Sanitised list
        """

        t = []
        for token in tokens:
            if token is UMin:
                t += [-1, Mul]
            else:
                t += [token]
        return t

    @staticmethod
    def _shunting_yard(tokens):
        """ Turns a statement in infix notation to RP (postfix) notation

            An implementation of Edsger Dijkstra's shunting-yard algorithm from the pseudo-code here:
            https://en.wikipedia.org/wiki/Shunting-yard_algorithm

            Args:
                tokens: A list of tokens to convert to RP notation, must be operators, numbers, or symbols

            Returns:
                A list of operators, numbers, and symbols in RPN

            Raises:
                SyntaxError: There were mismatched parenthesis in the expression
        """

        # TODO: Add type checking
        # TODO: Add function support?

        out_queue = deque()
        op_stack = []

        for token in tokens:
            # If the token is a number...
            if isinstance(token, (int, float, Symbol)):
                out_queue.append(token) # ...add it to the output queue

            # If the token is an operator...
            elif is_operator(token):
                # While there is an operator in the stack...
                while op_stack and is_operator(op_stack[-1]):
                    top_operator = op_stack[-1]
                    # ...if token is left-associative and its precedence is <= to that of the top operator...
                    if (token.association == 'left' and token.precedence <= top_operator.precedence or
                            # ...if the token is right associative, and has precedence less than that of the top operator...
                            token.association == 'right' and token.precedence < top_operator.precedence):
                        # ... pop it from the stack and push it to the queue
                        out_queue.append(op_stack.pop())
                        continue

                    break

                op_stack.append(token)

            # If token is a left parenthesis...
            elif token == '(':
                # ...push it to the queue
                op_stack.append('(')

            # If the token is a right parenthesis
            elif token == ')':
                # Until the the operator at the top of the stack is a left parenthesis...
                while op_stack and not op_stack[-1] == '(':
                    # ...pop operators off the stack onto the output queue
                    out_queue.append(op_stack.pop())
                # Pop the left parenthesis from the stack (but not onto the queue)
                op_stack.pop()

        # After all tokens are read...
        while op_stack:
            # If there are parenthesis still left on the stack
            if op_stack[-1] == '(' or op_stack[-1] == ')':
                raise SyntaxError('Mismatched parenthesis in expression ')
            out_queue.append(op_stack.pop())

        return list(out_queue)

    @staticmethod
    def _rpn_to_ast(rpn_list):
        """ Turns a statement in RP notation to an AST

            e.g: a b + ->       +
                              /  \
                             a    b
            Args:
                rpn_list: list of tokens in RP notation
            Returns:
                The root node of the AST
            Raises:
                TypeError: A unsupported type was passed
        """
        stack = []

        for token in rpn_list:
            # If the token is a number or symbol...
            if isinstance(token, (int, float, Symbol)):
                # ...add it to the stack as a node
                stack.append(Node(token))
            # If the token is a operator...
            elif is_operator(token):
                # ...get the top two operands...
                b = stack.pop()
                a = stack.pop()
                # ...add the operator as a node with the operand nodes as its children
                stack.append(Node(token, children=[a, b]))
            else:
                raise TypeError('Expected: number, symbol, or operator. Got {}'.format(type(token)))

        return stack[0]

    @staticmethod
    def _remove_subtraction(ast):
        """ Removes subtraction nodes from a tree, replacing them with equivalent commutative nodes.

        Expands a - b into a + (-1 * b), reducing the syntactic complexity of an AST

        e.g:         -                  +
                   /  \     ->        /  \
                  a    b             a    *
                                         / \
                                       -1   b

        Args:
            ast: The abstract syntax tree to perform the modification on

        Returns:
            The modified AST with all subtraction operators removed
        """
        for node in ast:
            if node.value == Sub:
                # Change the operation to +
                node.value = Add
                # store the left hand side of the expression
                b = node.children[1]
                # add the leaf nodes
                b.children = [Node(-1), Node(b.value)]
                # change the child operation to *
                b.value = Mul

        return ast

    @staticmethod
    def _level_operators(ast):
        """ Reduces nested binary commutative operators to a single non-binary node

        e.g:        +                   +
                  /  \                / | \
                 +    c     ->       a  b  c
               /  \
              a    b

        Args:
            ast: The abstract syntax tree to perform the modification on

        Returns:
            The modified AST with all commutative operations reduced
        """
        for node in ast:
            for child in node.children:
                # only works for commutative operators ( *, +)
                if is_commutative_operator(child.value) and child.value == node.value:
                    # Add the child's children to the parents children
                    node.children += child.children
                    # Remove the child from the children
                    node.children.remove(child)

        return ast

    @staticmethod
    def _simplify_rationals(ast):
        # TODO: Docstring

        for node in ast:
            # If fraction is numerator
            if is_operator(node.value, Div) and is_operator(node.children[0].value, Div):
                a = node.children[0].children[0]  # 2nd fraction numerator
                b = node.children[0].children[1]  # 2nd fraction denominator
                c = node.children[1]  # 1st fraction denominator

                node.children[0] = a  # a -> numerator
                node.children[1] = Node(Mul, [b, c])  # b * c -> denominator

            # If fraction is denominator
            elif is_operator(node.value, Div) and is_operator(node.children[1].value, Div):
                a = node.children[0]
                b = node.children[1].children[0]
                c = node.children[1].children[1]

                node.children[0] = Node(Mul, [a, b])
                node.children[1] = c

            # If fraction is multiplied
            elif is_operator(node.value, Mul) and in_children(node, Div):
                    first = in_children(node, Div)[0]
                    b = deepcopy(first.children[0])
                    c = deepcopy(first.children[1])
                    node.children.remove(first)
                    a = node.children[:]
                    node.children = [None]

                    node.value = Div
                    node.children[0] = Node(Mul, a + [b])
                    node.children += c

        return ast

    @staticmethod
    def _symbols_to_power_of_one(ast):
        for node in ast:
            if is_operator(node.value, Mul):
                for child in node.children:
                    if isinstance(child.value, Symbol):
                        child.children = [Node(child.value), Node(1)]
                        child.value = Pow

        return ast

    @staticmethod
    def _remove_powers_of_one(ast):
        for node in ast:
            if is_operator(node.value, Pow) and node.children[1] == Node(1):
                node.value = node.children[0]
                node.children = []

        return ast

    @staticmethod
    def _collect_like_powers(ast):

        # x -> x^1
        ast = Expression._symbols_to_power_of_one(ast)

        # TODO: Make more elegant?
        for node in ast:
            if is_operator(node.value, Mul) and in_children(node, Pow):

                exponentials = in_children(node, Pow)

                if len(exponentials) < 2:
                    continue

                node.children = [x for x in node.children if x not in exponentials]

                for exp in exponentials:
                    same_base = [other for other in exponentials if other.children[0] == exp.children[0]]

                    if len(same_base) < 2:
                        continue

                    # Merge all the nodes with the same base
                    final = combine_children(same_base)
                    # Make a list of powers (excluding the first base)
                    powers = final.children[1:]
                    # delete the powers
                    final.children[1:] = []
                    # remove all the bases from the children
                    powers = [x for x in powers if x != final.children[0]]
                    # Sum all the powers together
                    final.children.append(Node(Add, powers))
                    # get rid of exponentials just combined
                    exponentials = [x for x in exponentials if x not in same_base]
                    # add back to list of exponetials (in case of nested powers)
                    exponentials.append(final)

                node.children += exponentials

        # x^1 -> x
        ast = Expression._remove_powers_of_one(ast)

        return ast

    @staticmethod
    def _collect_like_addition(ast):

        for node in ast:
            if is_operator(node.value, Add) and instance_in_children(node, Symbol):
                symbols = instance_in_children(node, Symbol)

                if len(symbols) < 2:
                    continue

                node.children = [x for x in node.children if x not in symbols]

                for sym in symbols:
                    same_symbol = [other for other in symbols if other == sym]

                    if len(same_symbol) < 2:
                        continue

                    coefficent = len(same_symbol)
                    combined_node = Node(Mul, [Node(coefficent), same_symbol[0]])
                    symbols = [x for x in symbols if x not in same_symbol]
                    node.children.append(combined_node)

        return ast

    @staticmethod
    def fold_constants(ast):

        for node in ast:
            # x * 0 = 0
            if is_operator(node.value, Mul) and in_children(node, 0):
                node.value = 0
                node.children = []

            # x * 1 = x
            if is_operator(node.value, Mul) and in_children(node, 1):
                node.children = [x for x in node.children if x.value != 1]

            # y + x + 0 = x + y
            if is_operator(node.value, Add) and in_children(node, 0):
                node.children = [x for x in node.children if x.value != 0]

            # x^0 = 1, when x != 0
            if is_operator(node.value, Pow) and node.children[0].value != 0 and node.children[1].value == 0:
                node.value = 1
                node.children = []

            # 0^x = 0, when x != 0
            if is_operator(node.value, Pow) and node.children[0].value == 0 and node.children[1].value != 0:
                node.value = 0
                node.children = []

            # 1^x = 1
            if is_operator(node.value, Pow) and node.children[0].value == 1:
                node.value = 1
                node.children = []

            if (is_operator(node.value, Add) or is_operator(node.value, Mul)) and len(node.children) == 1:
                node.value = node.children[0].value
                node.children = node.children[0].children


        return ast

    @staticmethod
    def simplify_ast(ast):
        old_ast = None

        while old_ast != ast:
            old_ast = deepcopy(ast)

            ast = Expression._remove_subtraction(ast)
            ast = Expression._level_operators(ast)
            ast = Expression._simplify_rationals(ast)
            ast = Expression._collect_like_powers(ast)
            ast = Expression._collect_like_addition(ast)
            ast = Expression.fold_constants(ast)
        return ast

    ###

    def __init__(self, tokens):
        self.tokens = self.sanitise_unary(tokens)
        self.ast = self.build_ast(self.tokens)
        self.ast = Expression.simplify_ast(self.ast)

    def build_ast(self, token_list):
        return self._rpn_to_ast(self._shunting_yard(token_list))
