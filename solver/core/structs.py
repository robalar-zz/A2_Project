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
        yield self
        for child in self.children:
            for node in child:
                yield node


    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def set_parents(self):
        for child in self.children:
            child.parent = self
            child.set_parents()


from collections import deque

def breadth_first(node):

    if node is None:
        return

    queue = deque()
    queue.append(node)
    while queue:
        current_node = queue.pop()
        print current_node.value
        for child in node.children:
            queue.append(child)


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
