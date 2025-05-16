# -*- coding: utf-8 -*-
import pytest
import compas
import json

from compas.datastructures import Tree, TreeNode
from compas.data import json_dumps, json_loads

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def simple_tree():
    # A basic fixture for a simple tree
    root = TreeNode(name="root")
    branch1 = TreeNode(name="branch1")
    branch2 = TreeNode(name="branch2")
    leaf1_1 = TreeNode(name="leaf1_1")
    leaf1_2 = TreeNode(name="leaf1_2")
    leaf2_1 = TreeNode(name="leaf2_1")
    leaf2_2 = TreeNode(name="leaf2_2")

    tree = Tree()
    tree.add(root)
    tree.add(branch1, parent=root)
    tree.add(branch2, parent=root)
    tree.add(leaf1_1, parent=branch1)
    tree.add(leaf1_2, parent=branch1)
    tree.add(leaf2_1, parent=branch2)
    tree.add(leaf2_2, parent=branch2)
    return tree


# =============================================================================
# Basics
# =============================================================================


def test_treenode_initialization():
    node = TreeNode(name="test")
    assert node.name == "test"
    assert node.parent is None
    assert node.tree is None
    assert len(node.children) == 0


def test_tree_initialization():
    tree = Tree(name="test")
    assert tree.name == "test"
    assert tree.root is None


def test_empty_tree():
    tree = Tree()
    assert tree.root is None
    assert len(list(tree.nodes)) == 0
    assert len(list(tree.leaves)) == 0
    assert list(tree.traverse()) == []
    assert tree.get_hierarchy_string() == ""


# =============================================================================
# TreeNode Properties
# =============================================================================


def test_treenode_properties(simple_tree):
    root = simple_tree.root
    branch1, branch2 = list(root.children)
    leaf1_1, leaf1_2 = list(branch1.children)
    leaf2_1, leaf2_2 = list(branch2.children)

    assert root.is_root is True
    assert root.is_leaf is False
    assert root.is_branch is False

    assert branch1.is_root is False
    assert branch1.is_leaf is False
    assert branch1.is_branch is True

    assert branch2.is_root is False
    assert branch2.is_leaf is False
    assert branch2.is_branch is True

    assert leaf1_1.is_root is False
    assert leaf1_1.is_leaf is True
    assert leaf1_1.is_branch is False

    assert leaf1_2.is_root is False
    assert leaf1_2.is_leaf is True
    assert leaf1_2.is_branch is False

    assert leaf2_1.is_root is False
    assert leaf2_1.is_leaf is True
    assert leaf2_1.is_branch is False

    assert leaf2_2.is_root is False
    assert leaf2_2.is_leaf is True
    assert leaf2_2.is_branch is False


# =============================================================================
# Tree Properties
# =============================================================================


def test_tree_properties(simple_tree):
    nodes = list(simple_tree.nodes)
    leaves = list(simple_tree.leaves)

    assert len(nodes) == 7
    assert len(leaves) == 4


# =============================================================================
# Tree Traversal
# =============================================================================


def test_tree_traversal(simple_tree):
    nodes = [node.name for node in simple_tree.traverse(strategy="depthfirst", order="preorder")]
    assert nodes == ["root", "branch1", "leaf1_1", "leaf1_2", "branch2", "leaf2_1", "leaf2_2"]

    nodes = [node.name for node in simple_tree.traverse(strategy="depthfirst", order="postorder")]
    assert nodes == ["leaf1_1", "leaf1_2", "branch1", "leaf2_1", "leaf2_2", "branch2", "root"]

    nodes = [node.name for node in simple_tree.traverse(strategy="breadthfirst")]
    assert nodes == ["root", "branch1", "branch2", "leaf1_1", "leaf1_2", "leaf2_1", "leaf2_2"]


# =============================================================================
# Tree Manipulation
# =============================================================================


def test_tree_add_node(simple_tree):
    branch2 = simple_tree.get_node_by_name("branch2")
    branch2.add(TreeNode(name="test"))

    assert len(list(branch2.children)) == 3
    assert len(list(simple_tree.nodes)) == 8


def test_tree_remove_node(simple_tree):
    branch2 = simple_tree.get_node_by_name("branch2")
    leaf2_1 = simple_tree.get_node_by_name("leaf2_1")
    branch2.remove(leaf2_1)

    assert len(list(branch2.children)) == 1
    assert len(list(simple_tree.nodes)) == 6

    root = simple_tree.root
    branch1 = simple_tree.get_node_by_name("branch1")
    root.remove(branch1)

    assert len(list(root.children)) == 1
    assert len(list(simple_tree.nodes)) == 3


# =============================================================================
# Tree Serialization
# =============================================================================


def test_tree_serialization(simple_tree):
    serialized = json_dumps(simple_tree)
    deserialized = json_loads(serialized)
    assert simple_tree.__data__ == deserialized.__data__

    test_tree_properties(deserialized)
    test_tree_traversal(deserialized)
    test_tree_add_node(deserialized)
    test_tree_remove_node(json_loads(serialized))

    if not compas.IPY:
        data = json.loads(serialized)["data"]
        assert Tree.validate_data(data)


# =============================================================================
# Tree Conversion
# =============================================================================


def test_tree_to_graph(simple_tree):
    graph1 = simple_tree.to_graph()
    assert len(list(graph1.nodes())) == 7
    assert len(list(graph1.edges())) == 6
    assert graph1.has_edge((0, 1))
    assert graph1.has_edge((1, 2))
    assert graph1.has_edge((1, 3))
    assert graph1.has_edge((0, 4))
    assert graph1.has_edge((4, 5))
    assert graph1.has_edge((4, 6))

    def key_mapper(node):
        return node.name

    graph2 = simple_tree.to_graph(key_mapper)
    assert len(list(graph1.nodes())) == 7
    assert len(list(graph1.edges())) == 6
    assert graph2.has_edge(("root", "branch1"))
    assert graph2.has_edge(("branch1", "leaf1_1"))
    assert graph2.has_edge(("branch1", "leaf1_2"))
    assert graph2.has_edge(("root", "branch2"))
    assert graph2.has_edge(("branch2", "leaf2_1"))
    assert graph2.has_edge(("branch2", "leaf2_2"))


# =============================================================================
# TreeNode Representation
# =============================================================================


def test_treenode_representation(simple_tree):
    def node_repr(node):
        return node.name + "  CUSTOM STRING"
    print(simple_tree.get_hierarchy_string(node_repr=node_repr))

    assert simple_tree.get_hierarchy_string(node_repr=node_repr) == """└── root  CUSTOM STRING
    ├── branch1  CUSTOM STRING
    │   ├── leaf1_1  CUSTOM STRING
    │   └── leaf1_2  CUSTOM STRING
    └── branch2  CUSTOM STRING
        ├── leaf2_1  CUSTOM STRING
        └── leaf2_2  CUSTOM STRING"""
