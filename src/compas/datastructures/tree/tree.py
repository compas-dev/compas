# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data
from compas.datastructures import Datastructure


class TreeNode(Data):
    """A node of a tree data structure.

    Parameters
    ----------
    **kwargs : dict[str, Any], optional
        User-defined attributes of the tree node.

    Attributes
    ----------
    parent : :class:`compas.datastructures.TreeNode`
        The parent node of the tree node.
    children : list[:class:`compas.datastructures.TreeNode`]
        The children of the tree node.
    tree : :class:`compas.datastructures.Tree`
        The tree to which the node belongs.
    is_root : bool
        True if the node is the root node of the tree.
    is_leaf : bool
        True if the node is a leaf node of the tree.
    is_branch : bool
        True if the node is a branch node of the tree.
    acestors : generator[:class:`compas.datastructures.TreeNode`]
        A generator of the acestors of the tree node.
    descendants : generator[:class:`compas.datastructures.TreeNode`]
        A generator of the descendants of the tree node, using a depth-first preorder traversal.

    """

    DATASCHEMA = {
        "type": "object",
        "$recursiveAnchor": True,
        "properties": {
            "name": {"type": "string"},
            "attributes": {"type": "object"},
            "children": {"type": "array", "items": {"$recursiveRef": "#"}},
        },
    }

    @property
    def __data__(self):
        data = {}
        if self.name is not None:
            data["name"] = self.name
        if self.attributes:
            data["attributes"] = self.attributes
        if self.children:
            data["children"] = [child.__data__ for child in self.children]
        return data

    @classmethod
    def __from_data__(cls, data):
        name = data.get("name", None)
        attributes = data.get("attributes", {})
        children = data.get("children", [])

        node = cls(name=name, **attributes)
        for child in children:
            node.add(cls.__from_data__(child))
        return node

    def __init__(self, name=None, **kwargs):
        super(TreeNode, self).__init__(name=name)
        self.attributes = kwargs
        self._parent = None
        self._children = []
        self._tree = None

    def __repr__(self):
        if self._name:
            return "<TreeNode: {}>".format(self._name)
        return "<TreeNode>"

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
        if self.is_root:
            return self._tree
        else:
            return self.parent.tree  # type: ignore

    def add(self, node):
        """
        Add a child node to this node.

        Parameters
        ----------
        node : :class:`compas.datastructures.TreeNode`
            The node to add.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the node is not a :class:`compas.datastructures.TreeNode` object.

        """
        if not isinstance(node, TreeNode):
            raise TypeError("The node is not a TreeNode object.")
        if node not in self._children:
            self._children.append(node)
        node._parent = self

    def remove(self, node):
        """
        Remove a child node from this node.

        Parameters
        ----------
        node : :class:`compas.datastructures.TreeNode`
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
        while this.parent:
            yield this.parent
            this = this.parent

    @property
    def descendants(self):
        for child in self.children:
            yield child
            for descendant in child.descendants:
                yield descendant

    def traverse(self, strategy="depthfirst", order="preorder"):
        """
        Traverse the tree from this node.

        Parameters
        ----------
        strategy : {"depthfirst", "breadthfirst"}, optional
            The traversal strategy.
        order : {"preorder", "postorder"}, optional
            The traversal order. This parameter is only used for depth-first traversal.

        Yields
        ------
        :class:`compas.datastructures.TreeNode`
            The next node in the traversal.

        Raises
        ------
        ValueError
            If the strategy is not ``"depthfirst"`` or ``"breadthfirst"``.
            If the order is not ``"preorder"`` or ``"postorder"``.

        """
        if strategy == "depthfirst":
            if order == "preorder":
                yield self
                for child in self.children:
                    for node in child.traverse(strategy, order):
                        yield node
            elif order == "postorder":
                for child in self.children:
                    for node in child.traverse(strategy, order):
                        yield node
                yield self
            else:
                raise ValueError("Unknown traversal order: {}".format(order))
        elif strategy == "breadthfirst":
            queue = [self]
            while queue:
                node = queue.pop(0)
                yield node
                queue.extend(node.children)
        else:
            raise ValueError("Unknown traversal strategy: {}".format(strategy))


class Tree(Datastructure):
    """A hierarchical data structure that organizes elements into parent-child relationships.
    The tree starts from a unique root node, and every node (excluding the root) has exactly one parent.

    Parameters
    ----------
    name : str, optional
        The name of the tree.
    **kwargs : dict, optional
        Additional keyword arguments, which are stored in the attributes dict.

    Attributes
    ----------
    root : :class:`compas.datastructures.TreeNode`
        The root node of the tree.
    nodes : generator[:class:`compas.datastructures.TreeNode`]
        The nodes of the tree.
    leaves : generator[:class:`compas.datastructures.TreeNode`]
        A generator of the leaves of the tree.

    Examples
    --------
    >>> from compas.datastructures import Tree, TreeNode
    >>> tree = Tree()
    >>> root = TreeNode("root")
    >>> branch = TreeNode("branch")
    >>> leaf1 = TreeNode("leaf1")
    >>> leaf2 = TreeNode("leaf2")
    >>> tree.add(root)
    >>> root.add(branch)
    >>> branch.add(leaf1)
    >>> branch.add(leaf2)
    >>> print(tree)
    <Tree with 4 nodes>
        └── <TreeNode: root>
            └── <TreeNode: branch>
                ├── <TreeNode: leaf1>
                └── <TreeNode: leaf2>

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "root": TreeNode.DATASCHEMA,
            "attributes": {"type": "object"},
        },
        "required": ["root", "attributes"],
    }

    @property
    def __data__(self):
        return {
            "attributes": self.attributes,
            "root": self.root.__data__,  # type: ignore
        }

    @classmethod
    def __from_data__(cls, data):
        tree = cls()
        tree.attributes.update(data["attributes"] or {})
        root = TreeNode.__from_data__(data["root"])
        tree.add(root)
        return tree

    def __init__(self, name=None, **kwargs):
        super(Tree, self).__init__(kwargs, name=name)
        self._root = None

    def __str__(self):
        return "<Tree with {} nodes>\n{}".format(len(list(self.nodes)), self.get_hierarchy_string(max_depth=3))

    @property
    def root(self):
        return self._root

    def add(self, node, parent=None):
        """
        Add a node to the tree.

        Parameters
        ----------
        node : :class:`compas.datastructures.TreeNode`
            The node to add.
        parent : :class:`compas.datastructures.TreeNode`, optional
            The parent node of the node to add.
            Default is ``None``, in which case the node is added as a root node.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the node is not a :class:`compas.datastructures.TreeNode` object.
            If the supplied parent node is not a :class:`compas.datastructures.TreeNode` object.
        ValueError
            If the node is already part of another tree.
            If the supplied parent node is not part of this tree.
            If the tree already has a root node, when trying to add a root node.

        """
        if not isinstance(node, TreeNode):
            raise TypeError("The node is not a TreeNode object.")

        if node.parent:
            raise ValueError("The node already has a parent, remove it from that parent first.")

        if parent is None:
            # add the node as a root node
            if self.root is not None:
                raise ValueError("The tree already has a root node, remove it first.")

            self._root = node
            node._tree = self  # type: ignore

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

    def remove(self, node):
        """
        Remove a node from the tree.

        Parameters
        ----------
        node : :class:`compas.datastructures.TreeNode`
            The node to remove.

        Returns
        -------
        None

        """
        if node == self.root:
            self._root = None
            node._tree = None
        else:
            node.parent.remove(node)

    @property
    def leaves(self):
        for node in self.nodes:
            if node.is_leaf:
                yield node

    def traverse(self, strategy="depthfirst", order="preorder"):
        """
        Traverse the tree from the root node.

        Parameters
        ----------
        strategy : {"depthfirst", "breadthfirst"}, optional
            The traversal strategy.
        order : {"preorder", "postorder"}, optional
            The traversal order. This parameter is only used for depth-first traversal.

        Yields
        ------
        :class:`compas.datastructures.TreeNode`
            The next node in the traversal.

        Raises
        ------
        ValueError
            If the strategy is not ``"depthfirst"`` or ``"breadthfirst"``.
            If the order is not ``"preorder"`` or ``"postorder"``.

        """
        if self.root:
            for node in self.root.traverse(strategy=strategy, order=order):
                yield node

    def get_node_by_name(self, name):
        """
        Get a node by its name.

        Parameters
        ----------
        name : str
            The name of the node.

        Returns
        -------
        :class:`compas.datastructures.TreeNode`
            The node.

        """
        for node in self.nodes:
            if node.name == name:
                return node

    def get_nodes_by_name(self, name):
        """
        Get all nodes by their name.

        Parameters
        ----------
        name : str
            The name of the node.

        Returns
        -------
        list[:class:`compas.datastructures.TreeNode`]
            The nodes.

        """
        nodes = []
        for node in self.nodes:
            if node.name == name:
                nodes.append(node)
        return nodes

    def get_hierarchy_string(self, max_depth=None):
        """
        Return string representation for the spatial hierarchy of the tree.

        Parameters
        ----------
        max_depth : int, optional
            The maximum depth of the hierarchy to print.
            Default is ``None``, in which case the entire hierarchy is printed.

        Returns
        -------
        str
            String representing the spatial hierarchy of the tree.

        """

        hierarchy = []

        def traverse(node, hierarchy, prefix="", last=True, depth=0):
            if max_depth is not None and depth > max_depth:
                return

            connector = "└── " if last else "├── "
            hierarchy.append("{}{}{}".format(prefix, connector, node))
            prefix += "    " if last else "│   "
            for i, child in enumerate(node.children):
                traverse(child, hierarchy, prefix, i == len(node.children) - 1, depth + 1)

        if self.root:
            traverse(self.root, hierarchy)

        return "\n".join(hierarchy)

    def to_graph(self, key_mapper=None):
        """Convert the tree to a graph.

        Parameters
        ----------
        key_mapper : callable, optional
            A callable to map the tree node to a key in the graph.
            Default is ``None``, in which case the index of the node is used.

        Returns
        -------
        :class:`compas.datastructures.Graph`
            The graph.

        """
        from compas.datastructures import Graph

        graph = Graph(**self.attributes)
        nodes = list(self.nodes)

        if key_mapper is None:
            key_mapper = lambda node: nodes.index(node)  # noqa: E731

        for node in nodes:
            graph.add_node(key=key_mapper(node), attr_dict=node.attributes, name=node._name)

        for node in self.nodes:
            if node.parent:
                u = key_mapper(node.parent)
                v = key_mapper(node)
                graph.add_edge(u, v)

        return graph
