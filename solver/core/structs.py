from collections import deque


class ASTNode(object):

    def __init__(self, value, children=[]):
        self.value = value
        self.children = children
        self.parent = None

        # TODO: Fix recursion issue on parents
        """
        self.set_parents()
        """

    def __iter__(self):
        """Do a breadth first traversal of the tree"""
        if self is None:
            return

        queue = deque()
        queue.append(self)
        while queue:
            current_node = queue.pop()
            yield current_node
            for child in current_node.children:
                queue.append(child)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def set_parents(self):
        """for child in self.children:
            child.parent = self
            child.set_parents()"""
        pass


from collections import deque

def post_order(node):
    if node is not None:
        for child in node.children:
            post_order(child)
        print node.value


def postordereval(node):
    res1 = None
    res2 = None
    if node:
        res1 = postordereval(node.left)
        res2 = postordereval(node.right)
        if res1 and res2:
            return node.value(res1, res2)
        else:
            return node.value


def find_all(node, val):
    if node is not None:
        yield node
        for child in node.children:
            for n in find_all(child, val):
                yield n
