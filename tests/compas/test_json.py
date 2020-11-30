import numpy as np
import compas

from compas.geometry import Point, Vector, Frame
from compas.geometry import Box
from compas.geometry import Transformation

from compas.datastructures import Mesh


def test_dumps_native():
    data = [[], (), {}, '', 1, 1.0, True, None, float('inf')]
    s = compas.json_dumps(data)
    assert s == '[[], [], {}, "", 1, 1.0, true, null, Infinity]'


def test_dumps_numpy():
    data = [np.array([1, 2, 3]), np.array([1.0, 2.0, 3.0]), np.float64(1.0), np.int32(1), np.nan, np.inf]
    s = compas.json_dumps(data)
    assert s == '[[1, 2, 3], [1.0, 2.0, 3.0], 1.0, 1, NaN, Infinity]'


def test_dumps_primitive():
    d1 = Point(0, 0, 0)
    s1 = compas.json_dumps(d1)
    d2 = Point(np.float64(0.0), np.float64(0.0), np.float64(0.0))
    s2 = compas.json_dumps(d2)
    assert s1 == '{"dtype": "compas.geometry/Point", "value": [0.0, 0.0, 0.0]}'
    assert s2 == '{"dtype": "compas.geometry/Point", "value": [0.0, 0.0, 0.0]}'


def test_dumps_shape():
    d = Box(Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0)), 1, 1, 1)
    s = compas.json_dumps(d)
    _s = '{"dtype": "compas.geometry/Box", '
    _s += '"value": {"frame": {"point": [0.0, 0.0, 0.0], "xaxis": [1.0, 0.0, 0.0], "yaxis": [0.0, 1.0, 0.0]}, "xsize": 1.0, "ysize": 1.0, "zsize": 1.0}}'
    assert s == _s


def test_dumps_xform():
    d = Transformation.from_frame_to_frame(Frame.worldXY(), Frame.worldXY())
    s = compas.json_dumps(d)
    assert s == '{"dtype": "compas.geometry/Transformation", "value": {"matrix": [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]}}'


def test_dumps_mesh():
    d = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
    s = compas.json_dumps(d)
    _s = '{"dtype": "compas.datastructures/Mesh", '
    _s += '"value": {"compas": "0.17.3", "datatype": "compas.datastructures/Mesh", '
    _s += '"data": {"attributes": {"name": "Mesh"}, "dva": {"x": 0.0, "y": 0.0, "z": 0.0}, "dea": {}, "dfa": {}, '
    _s += '"vertex": {"0": {"x": 0, "y": 0, "z": 0}, "1": {"x": 1, "y": 0, "z": 0}, "2": {"x": 1, "y": 1, "z": 0}, "3": {"x": 0, "y": 1, "z": 0}}, '
    _s += '"face": {"0": [0, 1, 2, 3]}, "facedata": {"0": {}}, "edgedata": {}, "max_vertex": 3, "max_face": 0}}}'
    assert s == _s
