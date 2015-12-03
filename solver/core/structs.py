class ASTNode(object):

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return str(self.value)


def post_order(node):
    if node is not None:
        post_order(node.left)
        post_order(node.right)
        print node.value


def postordereval(node):
    res1 = None
    res2 = None
    if node:
        res1 = postordereval(node.left)
        res2 = postordereval(node.right)
        if res1 and res2:
            return node.value(res1, res2).result
        else:
            return node.value