class ASTNode(object):

    def __init__(self, value, children=[]):
        self.value = value
        self.children = children
        self.parent = None

        for child in self.children:
            child.parent = self

    def __iter__(self):
        yield self
        for child in self.children:
            for node in child:
                yield node


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


