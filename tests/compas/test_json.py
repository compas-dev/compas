import compas

from compas.geometry import Point, Vector, Frame
from compas.geometry import Box
from compas.geometry import Transformation

from compas.datastructures import Mesh


def test_json_native():
    before = [[], (), {}, '', 1, 1.0, True, None]
    after = compas.json_loads(compas.json_dumps(before))
    assert after == [[], [], {}, '', 1, 1.0, True, None]


if not compas.IPY:
    import numpy as np

    def test_json_numpy():
        before = [np.array([1, 2, 3]), np.array([1.0, 2.0, 3.0]), np.float64(1.0), np.int32(1)]
        after = compas.json_loads(compas.json_dumps(before))
        assert after == [[1, 2, 3], [1.0, 2.0, 3.0], 1.0, 1]


def test_json_primitive():
    before = Point(0, 0, 0)
    after = compas.json_loads(compas.json_dumps(before))
    assert isinstance(after, before.__class__)
    assert before.dtype == after.dtype
    assert all(a == b for a, b in zip(before, after))


def test_json_shape():
    before = Box(Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0)), 1, 1, 1)
    after = compas.json_loads(compas.json_dumps(before))
    assert isinstance(after, before.__class__)
    assert before.dtype == after.dtype
    assert all(a == b for a, b in zip(before.vertices, after.vertices))


def test_json_xform():
    before = Transformation.from_frame_to_frame(Frame.worldXY(), Frame.worldXY())
    after = compas.json_loads(compas.json_dumps(before))
    assert isinstance(after, before.__class__)
    assert before.dtype == after.dtype
    assert all(a == b for a, b in zip(before, after))


def test_json_mesh():
    before = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
    after = compas.json_loads(compas.json_dumps(before))
    assert isinstance(after, before.__class__)
    assert before.dtype == after.dtype
    assert all(before.has_vertex(vertex) for vertex in after.vertices())
    assert all(after.has_vertex(vertex) for vertex in before.vertices())
    assert all(before.has_face(face) for face in after.faces())
    assert all(after.has_face(face) for face in before.faces())
    assert all(before.has_edge(edge) for edge in after.edges())
    assert all(after.has_edge(edge) for edge in before.edges())
    assert all(before.face_vertices(a) == after.face_vertices(b) for a, b in zip(before.faces(), after.faces()))
