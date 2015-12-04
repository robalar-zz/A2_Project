from operations import *

__author__ = 'Rob'


class Symbol(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __add__(self, other):
        from expr import Expression
        return Expression([self, Add, other])
