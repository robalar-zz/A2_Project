from collections import deque
from copy import deepcopy

from structs import ASTNode, combine_children
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

            e.g:
            >>> Expression.sanitise_unary([UMin, 7])
            [-1, <class 'operations.Mul'>, 7]

            >>> Expression.sanitise_unary([5, Mul, UMin, 8])
            [5, <class 'operations.Mul'>, -1, <class 'operations.Mul'>, 8]
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

            Works with numerical statements...

            >>> Expression._shunting_yard([5, Add, 6])
            [5, 6, <class 'operations.Add'>]

            ...symbolic statements...

             >>> x = Symbol('x')
             >>> y = Symbol('y')
             >>> Expression._shunting_yard([x, Mul, y])
             [x, y, <class 'operations.Mul'>]

             ...brackets...

             >>> Expression._shunting_yard(['(', 5, Add, 6, ')', Mul, x])
             [5, 6, <class 'operations.Add'>, x, <class 'operations.Mul'>]

             ...functions are NYI.
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
        """
        stack = []

        for token in rpn_list:
            # If the token is a number or symbol...
            if isinstance(token, (int, float, Symbol)):
                # ...add it to the stack as a node
                stack.append(ASTNode(token))
            # If the token is a operator...
            elif issubclass(token, Operator):
                # ...get the top two operands...
                b = stack.pop()
                a = stack.pop()
                # ...add the operator as a node with the operand nodes as its children
                stack.append(ASTNode(token, children=[a, b]))

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
                b.children = [ASTNode(-1), ASTNode(b.value)]
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
                a = node.children[0].children[0]
                b = node.children[0].children[1]
                c = node.children[1]

                node.children[0] = a
                node.children[1] = ASTNode(Mul, [b, c])

            # If fraction is denominator
            elif is_operator(node.value, Div) and is_operator(node.children[1].value, Div):
                a = node.children[0]
                b = node.children[1].children[0]
                c = node.children[1].children[1]

                node.children[0] = ASTNode(Mul, [a, b])
                node.children[1] = c

            # If fraction is multiplied
            elif is_operator(node.value, Mul) and next((child for child in node.children if child.value == Div), None):
                    first = next(child for child in node.children if child.value == Div)
                    b = deepcopy(first.children[0])
                    c = deepcopy(first.children[1])
                    node.children.remove(first)
                    a = node.children[:]
                    node.children = [None]

                    node.value = Div
                    node.children[0] = ASTNode(Mul, a + [b])
                    node.children += c

        return ast

    @staticmethod
    def _collect_like_powers(ast):
        # TODO: Make more elegant?
        for node in ast:
            if is_operator(node.value, Mul) and next((child for child in node.children if child.value == Pow), None):

                exponentials = [child for child in node.children if child.value == Pow]
                node.children = [x for x in node.children if x not in exponentials]

                if len(exponentials) == 1:
                    break

                for exp in exponentials:
                    same_base = [other for other in exponentials if other.children[0] == exp.children[0]]

                    if len(same_base) < 2:
                        break

                    final = combine_children(same_base)
                    powers = final.children[1:]
                    del final.children[1:]
                    final.children += [ASTNode(Add, powers)]

                    exponentials = [x for x in exponentials if x not in same_base]
                    exponentials.append(final)

                node.children += exponentials

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
        return ast

    ###

    def __init__(self, tokens):
        self.tokens = self.sanitise_unary(tokens)
        self.ast = self.build_ast(self.tokens)
        self.ast = Expression.simplify_ast(self.ast)

    def build_ast(self, token_list):
        return self._rpn_to_ast(self._shunting_yard(token_list))
