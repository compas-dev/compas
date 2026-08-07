import pytest

from compas.data import json_dumps
from compas.data import json_loads
from compas.datastructures import HashNode
from compas.datastructures import HashTree
from compas.datastructures import Mesh
from compas.datastructures import Tree
from compas.datastructures import TreeNode


def test_hashtree_from_dict():
    tree1 = HashTree.from_dict({"a": {"b": 1, "c": 3}, "d": [1, 2, 3], "e": 2})
    tree2 = HashTree.from_dict({"a": {"b": 1, "c": 2}, "d": [1, 2, 3], "f": 2})
    diff = tree2.diff(tree1)

    assert diff["added"] == [{"path": ".f", "value": 2}]
    assert diff["removed"] == [{"path": ".e", "value": 2}]
    assert diff["modified"] == [{"path": ".a.c", "old": 3, "new": 2}]


def test_hashtree_from_mesh():
    mesh = Mesh.from_polyhedron(4)
    tree1 = HashTree.from_object(mesh)
    mesh.vertex_attribute(0, "x", 1.0)
    mesh.delete_face(3)
    tree2 = HashTree.from_object(mesh)
    diff = tree2.diff(tree1)

    assert diff["added"] == []
    assert diff["removed"] == [{"path": ".face.3", "value": [1, 3, 2]}, {"path": ".facedata.3", "value": None}]
    assert diff["modified"] == [{"path": ".vertex.0.x", "old": -0.8164965809277261, "new": 1.0}]


def test_hashtree_serialization():
    tree = HashTree.from_dict({"a": {"b": 1}, "c": [1, 2, 3]})

    other = json_loads(json_dumps(tree))

    assert isinstance(other, HashTree)
    assert all(isinstance(node, HashNode) for node in other.nodes)
    assert other.diff(tree) == {"added": [], "removed": [], "modified": []}
    assert other.signatures == tree.signatures


def test_empty_hashtree_serialization():
    tree = json_loads(json_dumps(HashTree()))

    assert isinstance(tree, HashTree)
    assert tree.root is None
    assert tree.signatures == {}


def test_hashnode_repr_computes_signature():
    node = HashNode(".a", value=1)

    assert repr(node) == ".a:1 @ {}".format(node.signature[:5])


def test_hashtree_from_object_requires_data():
    with pytest.raises(TypeError):
        HashTree.from_object({"a": 1})


def test_hashtree_diff_requires_roots():
    with pytest.raises(ValueError):
        HashTree().diff(HashTree())


def test_hashtree_signature_is_independent_of_dictionary_order():
    tree1 = HashTree.from_dict({"a": 1, "b": 2})
    tree2 = HashTree.from_dict({"b": 2, "a": 1})

    assert tree1.root.signature == tree2.root.signature


def test_hashtree_does_not_inherit_tree():
    assert not isinstance(HashTree(), Tree)
    assert not isinstance(HashNode(""), TreeNode)


def test_hashnode_children_are_immutable():
    child = HashNode(".a", value=1)
    root = HashNode("", children=[child])

    assert root.children == (child,)
    assert not hasattr(root, "add")

    with pytest.raises(AttributeError):
        root.path = ".changed"


def test_hashnode_value_is_defensively_copied():
    value = [1, 2]
    node = HashNode(".a", value=value)
    signature = node.signature

    value.append(3)
    returned_value = node.value
    returned_value.append(4)

    assert node.value == [1, 2]
    assert node.signature == signature


def test_hashnode_explicit_none_is_a_value():
    value_node = HashNode(".a", value=None)
    branch_node = HashNode(".a")

    assert value_node.is_value
    assert not branch_node.is_value
    assert value_node.signature != branch_node.signature


def test_hashnode_rejects_values_with_children():
    with pytest.raises(ValueError):
        HashNode("", value=1, children=[HashNode(".a", value=2)])


def test_hashnode_rejects_duplicate_child_paths():
    with pytest.raises(ValueError):
        HashNode("", children=[HashNode(".a", value=1), HashNode(".a", value=2)])


def test_hashtree_to_graph_rejects_duplicate_keys():
    tree = HashTree.from_dict({"a": 1, "b": 2})

    with pytest.raises(ValueError):
        tree.to_graph(lambda node: "duplicate")
