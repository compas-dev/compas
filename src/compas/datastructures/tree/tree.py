from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data import Data
from compas.datastructures import Graph


class TreeNode(Data):

    JSONSCHEMA = {}

    def __init__(self, tree):
        super(TreeNode, self).__init__()
        self._tree = tree
        self._attributes = {}
        self._parent = None

    @property
    def tree(self):
        return self._tree

    @property
    def attributes(self):
        return self._attributes

    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, node):
        assert node is None or isinstance(node, TreeNode)
        self._parent = node

    @property
    def children(self):
        pass

    @property
    def acestors(self):
        pass

    @property
    def descendants(self):
        pass

    def add_child(self, node):
        node._parent = self



class Tree(Graph):

    JSONSCHEMA = {}

    def __init__(self):
        super(Tree, self).__init__()
        self._attributes = {}
        assert self.is_valid
    
    @property
    def is_valid(self):
        pass

    @property
    def attributes(self):
        return self._attributes

    @property
    def root(self):
        pass

    @property
    def leaves(self):
        pass