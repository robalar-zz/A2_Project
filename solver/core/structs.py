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
