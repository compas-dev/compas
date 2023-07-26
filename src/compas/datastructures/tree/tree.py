from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Datastructure


class TreeNode(object):
    """A node of a tree data structure.

    Parameters
    ----------
    name: str, optional
        The name of the tree ndoe.
    attributes: dict[str, Any], optional
        User-defined attributes of the datastructure.

    Attributes
    ----------
    name: str
        The name of the datastructure.
    attributes : dict[str, Any]
        User-defined attributes of the datastructure.
    parent: :class:`~compas.datastructures.TreeNode`
        The parent node of the tree node.
    children: set[:class:`~compas.datastructures.TreeNode`]
        The children of the tree node.
    tree: :class:`~compas.datastructures.Tree`
        The tree the node belongs to.
    is_root: bool
        True if the node is the root node of the tree.
    is_leaf: bool
        True if the node is a leaf node of the tree.
    is_branch: bool
        True if the node is a branch node of the tree.
    acestors: generator[:class:`~compas.datastructures.TreeNode`]
        A generator of the acestors of the tree node.
    descendants: generator[:class:`~compas.datastructures.TreeNode`]
        A generator of the descendants of the tree node.

    """

    def __init__(self, name=None, attributes=None):
        self.name = name
        self.attributes = attributes or {}
        self._parent = None
        self._children = set()
        self._tree = None

    def __repr__(self):
        return "<TreeNode {}>".format(self.name)

    @property
    def is_root(self):
        return self._parent is None

    @property
    def is_leaf(self):
        return not self._children

    @property
    def is_branch(self):
        return not self.is_root and not self.is_leaf

    @property
    def parent(self):
        return self._parent

    @property
    def children(self):
        return self._children

    @property
    def tree(self):
        return self._tree

    def add(self, node):
        """Add a child node to this node."""
        if not isinstance(node, TreeNode):
            raise TypeError("The node is not a TreeNode object.")
        self._children.add(node)
        node._parent = self
        node._tree = self.tree
        if self.tree:
            self.tree.nodes.add(node)

    def remove(self, node):
        """Remove a child node from this node."""
        self._children.remove(node)
        node._parent = None
        node._tree = None
        if self.tree:
            self.tree.nodes.remove(node)

    @property
    def ancestors(self):
        this = self
        while this:
            yield this
            this = this.parent

    @property
    def descendants(self):
        for child in self.children:
            yield child
            for descendant in child.descendants:
                yield descendant

    def traverse(self, strategy="preorder"):
        """Traverse the tree from this node."""
        if strategy == "preorder":
            yield self
            for child in self.children:
                for node in child.traverse(strategy):
                    yield node
        elif strategy == "postorder":
            for child in self.children:
                for node in child.traverse(strategy):
                    yield node
            yield self
        else:
            raise ValueError("Unknown traversal strategy: {}".format(strategy))


class Tree(Datastructure):
    """A tree data structure.

    Parameters
    ----------
    name: str, optional
        The name of the datastructure.
    attributes: dict[str, Any], optional
        User-defined attributes of the datastructure.

    Attributes
    ----------
    name: str
        The name of the datastructure.
    attributes : dict[str, Any]
        User-defined attributes of the datastructure.
    root: :class:`~compas.datastructures.TreeNode`
        The root node of the tree.
    nodes: set[:class:`~compas.datastructures.TreeNode`]
        The nodes of the tree.
    leaves: generator[:class:`~compas.datastructures.TreeNode`]
        A generator of the leaves of the tree.

    Examples
    --------
    >>> from compas.datastructures import Tree, TreeNode
    >>> tree = Tree()
    >>> root = TreeNode('root')
    >>> branch = TreeNode('branch')
    >>> leaf1 = TreeNode('leaf1')
    >>> leaf2 = TreeNode('leaf2')
    >>> tree.add_root(root)
    >>> root.add(branch)
    >>> branch.add(leaf1)
    >>> branch.add(leaf2)
    >>> print(tree)
    <Tree with 4 nodes, 1 branches, and 2 leaves>
    >>> tree.print()
    <TreeNode root>
        <TreeNode branch>
            <TreeNode leaf2>
            <TreeNode leaf1>

    """

    JSONSCHEMA = {}

    def __init__(self, name=None, attributes=None):
        super(Tree, self).__init__()
        self.name = name
        self.attributes = attributes or {}
        self._root = None
        self._nodes = set()

    @property
    def data(self):
        def get_node_data(node):
            return {
                "name": node.name,
                "attributes": node.attributes,
                "children": [get_node_data(child) for child in node.children],
            }

        return {
            "name": self.name,
            "root": get_node_data(self.root),
            "attributes": self.attributes,
        }

    @data.setter
    def data(self, data):
        self.name = data["name"]
        self.attributes = data["attributes"]

        def node_from_data(data):
            node = TreeNode(data["name"], data["attributes"])
            for child in data["children"]:
                node.add(node_from_data(child))
            return node

        self.add_root(node_from_data(data["root"]))

    @property
    def root(self):
        return self._root

    def add_root(self, node):
        """Add a root node to the tree."""
        if not isinstance(node, TreeNode):
            raise TypeError("The node is not a TreeNode object.")
        if not node.is_root:
            raise ValueError("The node is already part of another tree.")
        self._root = node
        node._tree = self
        self._nodes.add(node)

    def add(self, node, parent):
        """Add a node to the tree."""
        if not isinstance(node, TreeNode):
            raise TypeError("The node is not a TreeNode object.")
        if self.root is None:
            raise ValueError("The tree has no root node, use add_root() first.")
        else:
            parent.add(node)

    @property
    def nodes(self):
        return self._nodes

    def _remove_root(self):
        """Remove the root node from the tree."""
        self._root._tree = None
        self.nodes.remove(self._root)
        self._root = None

    def remove(self, node):
        """Remove a node from the tree."""
        if node == self.root:
            self._remove_root()
        else:
            node.parent.remove(node)

    @property
    def leaves(self):
        for node in self.nodes:
            if node.is_leaf:
                yield node

    def __repr__(self):
        return "<Tree with {} nodes>".format(len(self.nodes))

    def print(self):
        """Print the spatial hierarchy of the tree."""

        def _print(node, depth=0):
            print("  " * depth + str(node))
            for child in node.children:
                _print(child, depth + 1)

        _print(self.root)
