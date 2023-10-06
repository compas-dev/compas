from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Datastructure
from compas.data import Data


class TreeNode(Data):
    """A node of a tree data structure.

    Parameters
    ----------
    name : str, optional
        The name of the tree ndoe.
    attributes : dict[str, Any], optional
        User-defined attributes of the datastructure.

    Attributes
    ----------
    name : str
        The name of the datastructure.
    attributes : dict[str, Any]
        User-defined attributes of the datastructure.
    parent : :class:`~compas.datastructures.TreeNode`
        The parent node of the tree node.
    children : set[:class:`~compas.datastructures.TreeNode`]
        The children of the tree node.
    is_root : bool
        True if the node is the root node of the tree.
    is_leaf : bool
        True if the node is a leaf node of the tree.
    is_branch : bool
        True if the node is a branch node of the tree.
    acestors : generator[:class:`~compas.datastructures.TreeNode`]
        A generator of the acestors of the tree node.
    descendants : generator[:class:`~compas.datastructures.TreeNode`]
        A generator of the descendants of the tree node.

    """

    DATASCHEMA = {
        "type": "object",
        "$recursiveAnchor": True,
        "properties": {
            "name": {"type": "string"},
            "attributes": {"type": "object"},
            "children": {"type": "array", "items": {"$recursiveRef": "#"}},
        },
        "required": ["name", "attributes", "children"],
    }

    def __init__(self, name=None, attributes=None):
        super(TreeNode, self).__init__(name=name)
        self.attributes = attributes or {}
        self._parent = None
        self._children = set()

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
    def data(self):
        return {
            "name": self.name,
            "attributes": self.attributes,
            "children": [child.data for child in self.children],
        }

    @classmethod
    def from_data(cls, data):
        node = cls(data["name"], data["attributes"])
        for child in data["children"]:
            node.add(cls.from_data(child))
        return node

    def add(self, node):
        """
        Add a child node to this node.

        Parameters
        ----------
        node : :class:`~compas.datastructures.TreeNode`
            The node to add.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the node is not a :class:`~compas.datastructures.TreeNode` object.

        """
        if not isinstance(node, TreeNode):
            raise TypeError("The node is not a TreeNode object.")
        self._children.add(node)
        node._parent = self

    def remove(self, node):
        """
        Remove a child node from this node.

        Parameters
        ----------
        node : :class:`~compas.datastructures.TreeNode`
            The node to remove.

        Returns
        -------
        None

        """
        self._children.remove(node)
        node._parent = None

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
        """
        Traverse the tree from this node.

        Parameters
        ----------
        strategy : str, optional
            The traversal strategy. Options are ``"preorder"`` and ``"postorder"``.
            Default is ``"preorder"``.

        Yields
        ------
        :class:`~compas.datastructures.TreeNode`
            The next node in the traversal.

        Raises
        ------
        ValueError
            If the strategy is not ``"preorder"`` or ``"postorder"``.

        """
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
    name : str, optional
        The name of the datastructure.
    attributes : dict[str, Any], optional
        User-defined attributes of the datastructure.

    Attributes
    ----------
    name : str
        The name of the datastructure.
    attributes : dict[str, Any]
        User-defined attributes of the datastructure.
    root : :class:`~compas.datastructures.TreeNode`
        The root node of the tree.
    nodes : list[:class:`~compas.datastructures.TreeNode`]
        The nodes of the tree.
    leaves : generator[:class:`~compas.datastructures.TreeNode`]
        A generator of the leaves of the tree.

    Examples
    --------
    >>> from compas.datastructures import Tree, TreeNode
    >>> tree = Tree()
    >>> root = TreeNode('root')
    >>> branch = TreeNode('branch')
    >>> leaf1 = TreeNode('leaf1')
    >>> leaf2 = TreeNode('leaf2')
    >>> tree.add(root)
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

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "root": TreeNode.DATASCHEMA,
            "attributes": {"type": "object"},
        },
        "required": ["name", "root", "attributes"],
    }

    def __init__(self, name=None, attributes=None):
        super(Tree, self).__init__()
        self.name = name
        self.attributes = attributes or {}
        self._root = None

    @property
    def data(self):
        return {
            "name": self.name,
            "root": self.root.data,
            "attributes": self.attributes,
        }

    @classmethod
    def from_data(cls, data):
        tree = cls(data["name"], data["attributes"])
        root = TreeNode.from_data(data["root"])
        tree.add(root)
        return tree

    @property
    def root(self):
        return self._root

    def add(self, node, parent=None):
        """
        Add a node to the tree.

        Parameters
        ----------
        node : :class:`~compas.datastructures.TreeNode`
            The node to add.
        parent : :class:`~compas.datastructures.TreeNode`, optional
            The parent node of the node to add.
            Default is ``None``, in which case the node is added as a root node.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the node is not a :class:`~compas.datastructures.TreeNode` object.
            If the supplied parent node is not a :class:`~compas.datastructures.TreeNode` object.
        ValueError
            If the node is already part of another tree.
            If the supplied parent node is not part of this tree.
            If the tree already has a root node, when trying to add a root node.

        """
        if not isinstance(node, TreeNode):
            raise TypeError("The node is not a TreeNode object.")

        if node.parent:
            raise ValueError("The node is already part of another tree, remove it from that tree first.")

        if parent is None:
            # add the node as a root node
            if self.root is not None:
                raise ValueError("The tree already has a root node, remove it first.")

            self._root = node

        else:
            # add the node as a child of the parent node
            if not isinstance(parent, TreeNode):
                raise TypeError("The parent node is not a TreeNode object.")

            if parent.tree is not self:
                raise ValueError("The parent node is not part of this tree.")

            parent.add(node)

    @property
    def nodes(self):
        if self.root:
            for node in self.root.traverse():
                yield node
        else:
            yield iter([])

    def remove(self, node):
        """
        Remove a node from the tree.

        Parameters
        ----------
        node : :class:`~compas.datastructures.TreeNode`
            The node to remove.

        Returns
        -------
        None

        """
        if node == self.root:
            self._root = None
        else:
            node.parent.remove(node)

    @property
    def leaves(self):
        for node in self.nodes:
            if node.is_leaf:
                yield node

    def __repr__(self):
        return "<Tree with {} nodes>".format(len(list(self.nodes)))

    def print(self):
        """Print the spatial hierarchy of the tree."""

        def _print(node, depth=0):
            print("  " * depth + str(node))
            for child in node.children:
                _print(child, depth + 1)

        _print(self.root)
