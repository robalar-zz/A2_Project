class ASTNode(object):

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def get_children_recursive(self, level=0):
        children = [self.left, self.right]
        string = '{0}{1}\n'.format('\t'*level, self.value)
        for child in children:
            if child is not None:
                string += child.get_children_recursive(level+1)
        return string
