# -*- coding: utf-8 -*-
import hashlib

from compas.data import Data
from compas.data import json_dumps
from compas.datastructures import Tree
from compas.datastructures import TreeNode


class HashNode(TreeNode):
    """A node in a HashTree. This class is used internally by the HashTree class.

    Parameters
    ----------
    path : str
        The relative path of the node.
    value : str, int, float, list, bool, None
        The value of the node. Only leaf nodes can have a value.

    Attributes
    ----------
    path : str
        The relative path of the node.
    value : str, int, float, list, bool, None
        The value of the node. Only leaf nodes can have a value.
    absolute_path : str
        The absolute path of the node.
    is_value : bool
        True if the node is a leaf node and has a value.
    signature : str
        The SHA256 signature of the node.
    children_dict : dict
        A dictionary of the children of the node. The keys are the relative paths
    children_paths : list[str]
        A list of the relative paths of the children of the node.

    """

    def __init__(self, path, value=None, **kwargs):
        super(HashNode, self).__init__(**kwargs)
        self.path = path
        self.value = value
        self._signature = None

    def __repr__(self):
        path = self.path or "ROOT"
        if self.value is not None:
            return "{}:{} @ {}".format(path, self.value, self.signature[:5])
        else:
            return "{} @ {}".format(path, self.signature[:5])

    @property
    def absolute_path(self):
        if self.parent is None:
            return self.path
        return self.parent.absolute_path + self.path

    @property
    def is_value(self):
        return self.value is not None

    @property
    def signature(self):
        return self._signature

    @property
    def children_dict(self):
        return {child.path: child for child in self.children}

    @property
    def children_paths(self):
        return [child.path for child in self.children]

    @classmethod
    def from_dict(cls, data_dict, path=""):
        """Construct a HashNode from a dictionary.

        Parameters
        ----------
        data_dict : dict
            A dictionary to construct the HashNode from.
        path : str
            The relative path of the node.

        Returns
        -------
        :class:`compas.datastructures.HashNode`
            A HashNode constructed from the dictionary.

        """
        node = cls(path)
        for key in data_dict:
            path = ".{}".format(key)
            if isinstance(data_dict[key], dict):
                child = cls.from_dict(data_dict[key], path=path)
                node.add(child)
            else:
                node.add(cls(path, value=data_dict[key]))

        return node


class HashTree(Tree):
    """HashTree data structure to compare differences in hierarchical data.

    A Hash tree (or Merkle tree) is a tree in which every leaf node is labelled with the cryptographic hash
    of a data block and every non-leaf node is labelled with the hash of the labels of its child nodes.
    Hash trees allow efficient and secure verification of the contents of large data structures.
    They can also be used to compare different versions(states) of the same data structure for changes.

    Attributes
    ----------
    signatures : dict[str, str]
        The SHA256 signatures of the nodes in the tree. The keys are the absolute paths of the nodes, the values are the signatures.

    Examples
    --------
    >>> tree1 = HashTree.from_dict({"a": {"b": 1, "c": 3}, "d": [1, 2, 3], "e": 2})
    >>> tree2 = HashTree.from_dict({"a": {"b": 1, "c": 2}, "d": [1, 2, 3], "f": 2})
    >>> print(tree1)
    +-- ROOT @ 4cd56
        +-- .a @ c16fd
        |   +-- .b:1 @ c9b55
        |   +-- .c:3 @ 518d4
        +-- .d:[1, 2, 3] @ 9be3a
        +-- .e:2 @ 68355
    >>> print(tree2)
    +-- ROOT @ fbe39
        +-- .a @ c2022
        |   +-- .b:1 @ c9b55
        |   +-- .c:2 @ e3365
        +-- .d:[1, 2, 3] @ 9be3a
        +-- .f:2 @ 93861
    >>> tree2.print_diff(tree1)
    Added:
    {'path': '.f', 'value': 2}
    Removed:
    {'path': '.e', 'value': 2}
    Modified:
    {'path': '.a.c', 'old': 3, 'new': 2}

    """

    def __init__(self, **kwargs):
        super(HashTree, self).__init__(**kwargs)
        self.signatures = {}

    @classmethod
    def from_dict(cls, data_dict):
        """Construct a HashTree from a dictionary.

        Parameters
        ----------
        data_dict : dict
            A dictionary to construct the HashTree from.

        Returns
        -------
        :class:`compas.datastructures.HashTree`
            A HashTree constructed from the dictionary.

        """
        tree = cls()
        root = HashNode.from_dict(data_dict)
        tree.add(root)
        tree.node_signature(tree.root)
        return tree

    @classmethod
    def from_object(cls, obj):
        """Construct a HashTree from a COMPAS data object."""
        if not isinstance(obj, Data):
            raise TypeError("The object must be a COMPAS data object.")
        return cls.from_dict(obj.__data__)

    def node_signature(self, node, parent_path=""):
        """Compute the SHA256 signature of a node. The computed nodes are cached in `self.signatures` dictionary.

        Parameters
        ----------
        node : :class:`compas.datastructures.HashNode`
            The node to compute the signature of.
        parent_path : str
            The absolute path of the parent node.

        Returns
        -------
        str
            The SHA256 signature of the node.

        """
        absolute_path = parent_path + node.path
        if absolute_path in self.signatures:
            return self.signatures[absolute_path]

        content = {
            "path": node.path,
            "value": node.value,
            "children": [self.node_signature(child, absolute_path) for child in node.children],
        }

        signature = hashlib.sha256(json_dumps(content).encode()).hexdigest()

        self.signatures[absolute_path] = signature
        node._signature = signature

        return signature

    def diff(self, other):
        """Compute the difference between two HashTrees.

        Parameters
        ----------
        other : :class:`compas.datastructures.HashTree`
            The HashTree to compare with.

        Returns
        -------
        dict
            A dictionary containing the differences between the two HashTrees. The keys are `added`, `removed` and `modified`.
            The values are lists of dictionaries containing the paths and values of the nodes that were added, removed or modified.
        """
        added = []
        removed = []
        modified = []

        def _diff(node1, node2):
            if node1.signature == node2.signature:
                return
            else:
                if node1.is_value or node2.is_value:
                    modified.append({"path": node1.absolute_path, "old": node2.value, "new": node1.value})

                for path in node1.children_paths:
                    if path in node2.children_dict:
                        _diff(node1.children_dict[path], node2.children_dict[path])
                    else:
                        added.append({"path": node1.children_dict[path].absolute_path, "value": node1.children_dict[path].value})

                for path in node2.children_paths:
                    if path not in node1.children_dict:
                        removed.append({"path": node2.children_dict[path].absolute_path, "value": node2.children_dict[path].value})

        _diff(self.root, other.root)

        return {"added": added, "removed": removed, "modified": modified}

    def print_diff(self, other):
        """Print the difference between two HashTrees.

        Parameters
        ----------
        other : :class:`compas.datastructures.HashTree`
            The HashTree to compare with.

        """

        diff = self.diff(other)
        print("Added:")
        for item in diff["added"]:
            print(item)
        print("Removed:")
        for item in diff["removed"]:
            print(item)
        print("Modified:")
        for item in diff["modified"]:
            print(item)
