from collections import deque


class Node(object):
    """ Class to represent node in a tree.

    A non-binary node that can have multiple children

    Attributes:
        value: The data contained in the node, can be any type.
        children: A list of other Node classes that are the children (connected to) the node
        parent: NYI
    """

    def __init__(self, value, children=[]):
        self.value = value
        self.children = children
        self.parent = None

        # TODO: Fix recursion issue on parents
        """
        self.set_parents()
        """

    def __iter__(self):
        """Do a breadth first traversal of the tree.

        Traverse the tree top-down left to right, yielding at each node.
        """

        queue = deque()
        queue.append(self)
        while queue:
            current_node = queue.pop()
            yield current_node
            for child in current_node.children:
                queue.append(child)

    def __eq__(self, other):
        """ Works as expected...
        >>> Node(8) == Node(8)
        True
        >>> Node(8) == Node(7)
        False
        >>> Node(8) == 'x'
        False

        ...also recursively checks children for equality...
        >>> Node(8, [Node(7, [Node(5), Node(4)]), Node(6, [Node(3), Node(2)])]) == Node(8, [Node(7, [Node(5), Node(4)]), Node(6, [Node(3), Node(2)])])
        True
        """

        if isinstance(other, Node):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.value)

    # FIXME
    def set_parents(self):
        for child in self.children:
            child.parent = self
            child.set_parents()


def combine_children(list_of_nodes):
    """ Merges the children of the nodes provided into the children of the first node provided (base node).

    This method DOES NOT preserve the value of the other nodes, just the base node!!!

    Args:
        list_of_nodes: Nodes to merge.
    Returns:
        base_node: Node containing all the children of the other nodes.

    >>> n = Node(1, [Node(2), Node(3)])
    >>> n2 = Node(4, [Node(5), Node(6)])
    >>> combine_children([n, n2]).children
    [2, 3, 5, 6]
    """
    if len(list_of_nodes) == 1:
        return list_of_nodes[0]

    base_node = list_of_nodes[0]
    for node in list_of_nodes[1:]:
        for child in node.children:
            base_node.children.append(child)

    return base_node


def in_children(node, value):
    """ Returns the child nodes which have the value of value

    Args:
        node: Node to search in
        value: Value to try and match
    Returns: List of matching nodes

    >>> n = Node('a', [Node('b'), Node(9), Node(9)])
    >>> in_children(n, 9)
    [9, 9]
    """
    return [child for child in node.children if child.value == value]


def instance_in_children(node, cls):
    return [child for child in node.children if isinstance(child.value, cls)]
