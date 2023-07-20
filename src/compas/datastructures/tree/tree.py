from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import annotations

from compas.data import Data
from compas.datastructures import Datastructure


class TreeNode(Data):
    JSONSCHEMA = {}

    def __init__(self, name: str = None, attributes: dict = None):
        super(TreeNode, self).__init__(name=name)
        self.attributes = attributes or {}
        self._parent = None
        self._children = set()

    def __repr__(self) -> str:
        return "TreeNode({})".format(self.name)

    @property
    def data(self):
        return {
            "name": self.name,
            "attributes": self.attributes,
            "parent": str(self.parent.guid) if self.parent else None,
            "children": [str(child.guid) for child in self.children],
        }

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
        return list(self._children)

    def add(self, node: TreeNode):
        assert isinstance(node, TreeNode), "The node is not a TreeNode object."
        self._children.add(node)
        node._parent = self

    @property
    def remove(self, node: TreeNode):
        self._children.remove(node)
        node._parent = None

    @property
    def acestors(self):
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

    def traverse(self):
        yield self
        for descendant in self.descendants:
            yield descendant


class Tree(Datastructure):
    JSONSCHEMA = {}

    def __init__(self):
        super(Tree, self).__init__()
        self.attributes = {}
        self._root = None

    @property
    def data(self):
        return {
            "root": str(self.root.guid) if self.root else None,
            "nodes": [node.data for node in self.nodes],
        }

    @property
    def root(self):
        return self._root

    def add_root(self, node: TreeNode):
        assert isinstance(node, TreeNode), "The node is not a TreeNode object."
        if not node.is_root:
            raise ValueError("The node is already part of another tree.")
        self._root = node

    def add(self, node: TreeNode, parent: TreeNode):
        assert isinstance(node, TreeNode), "The node is not a TreeNode object."
        if self.root is None:
            raise ValueError("The tree has no root node, use add_root() first.")
        else:
            parent.add(node)

    @property
    def nodes(self):
        return list(self.root.traverse())

    def remove(self, node: TreeNode):
        if node.is_root:
            self._root = None
        else:
            node.parent.remove(node)

    @property
    def leaves(self):
        for node in self.nodes:
            if node.is_leaf:
                yield node

    def summary(self):
        nodes = len(self.nodes)
        branches = sum(1 for node in self.nodes if node.is_branch)
        leaves = sum(1 for node in self.nodes if node.is_leaf)
        print("Tree with {} nodes, {} branches, and {} leaves".format(nodes, branches, leaves))

    def print(self):
        def _print(node, depth=0):
            print("  " * depth + str(node))
            for child in node.children:
                _print(child, depth + 1)

        _print(self.root)


if __name__ == "__main__":
    from compas.data import json_dumps

    R = TreeNode("R")
    B = TreeNode("B")
    L = TreeNode("L")
    L2 = TreeNode("L2")

    T = Tree()
    T.add_root(R)

    # T.add(B, R)
    # T.add(L, B)
    # T.add(L2, B)

    R.add(B)
    B.add(L)
    B.add(L2)

    # T.print()

    print(json_dumps(T, pretty=True))
