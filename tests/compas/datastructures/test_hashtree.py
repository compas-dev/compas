from compas.datastructures import HashTree
from compas.datastructures import Mesh


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
