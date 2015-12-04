from collections import deque

from structs import ASTNode, post_order
from symbol import Symbol, is_operator, is_commutative_operator
from operations import *

__author__ = 'Robert Hales'


class Expression(object):

    def __init__(self, tokens):
        self.tokens = self.sanitise_unary(tokens)

        self.ast = self.build_ast(self.tokens)
        self.ast = self._remove_subtraction(self.ast)
        self.ast = self._level_operators(self.ast)

    def __repr__(self):
        return str(self.tokens)

    @staticmethod
    def sanitise_unary(tokens):
        t = []
        for token in tokens:
            if token is UMin:
                t += [-1, Mul]
            else:
                t += [token]
        return t

    def _shunting_yard(self, tokens):

        """
        An implementation of Edsger Dijkstra's shunting-yard algorithm from the psudo-code here:
            https://en.wikipedia.org/wiki/Shunting-yard_algorithm
        """

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
            if op_stack[-1] == '(' or op_stack[-1] == ')':
                raise Exception('Mismatched parenthesis in expression ')
            out_queue.append(op_stack.pop())

        return list(out_queue)

    def _rpn_to_ast(self, rpn_list):

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

    def build_ast(self, token_list):
        return self._rpn_to_ast(self._shunting_yard(token_list))

    @staticmethod
    def _remove_subtraction(ast):
        for node in ast:
            if node.value == Sub:
                node.value = Add
                b = node.children[1]
                b.children = [ASTNode(-1), ASTNode(b.value)]
                b.value = Mul

        return ast

    @staticmethod
    def _level_operators(ast):
        for node in ast:
            for child in node.children:
                # only works for commutative operators ( *, +)
                if is_commutative_operator(child.value) and child.value == node.value:
                    # Add the child's children to the parents children
                    node.children += child.children
                    # Remove the child from the children
                    node.children.remove(child)

        return ast
