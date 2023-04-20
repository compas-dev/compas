import compas
from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.datastructures import VolMesh
from compas.geometry import Box
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Transformation
from compas.geometry import Vector


def test_json_native():
    before = [[], (), {}, "", 1, 1.0, True, None]
    after = compas.json_loads(compas.json_dumps(before))
    assert after == [[], [], {}, "", 1, 1.0, True, None]


def test_json_primitive():
    before = Point(0, 0, 0)
    after = compas.json_loads(compas.json_dumps(before))
    assert before.dtype == after.dtype
    assert all(a == b for a, b in zip(before, after))
    assert before.guid == after.guid


def test_json_shape():
    before = Box(Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0)), 1, 1, 1)
    after = compas.json_loads(compas.json_dumps(before))
    assert before.dtype == after.dtype
    assert all(a == b for a, b in zip(before.vertices, after.vertices))
    assert before.guid == after.guid


def test_json_xform():
    before = Transformation.from_frame_to_frame(Frame.worldXY(), Frame.worldXY())
    after = compas.json_loads(compas.json_dumps(before))
    assert before.dtype == after.dtype
    assert all(a == b for a, b in zip(before, after))
    assert before.guid == after.guid


def test_json_network():
    before = Network()
    a = before.add_node()
    b = before.add_node()
    before.add_edge(a, b)
    after = compas.json_loads(compas.json_dumps(before))
    assert before.dtype == after.dtype
    assert before.attributes == after.attributes
    assert all(before.has_node(node) for node in after.nodes())
    assert all(after.has_node(node) for node in before.nodes())
    assert all(before.has_edge(*edge) for edge in after.edges())
    assert all(after.has_edge(*edge) for edge in before.edges())
    assert before.guid == after.guid


def test_json_mesh():
    before = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
    after = compas.json_loads(compas.json_dumps(before))
    assert before.dtype == after.dtype
    assert before.attributes == after.attributes
    assert all(before.has_vertex(vertex) for vertex in after.vertices())
    assert all(after.has_vertex(vertex) for vertex in before.vertices())
    assert all(before.has_face(face) for face in after.faces())
    assert all(after.has_face(face) for face in before.faces())
    assert all(before.has_edge(edge) for edge in after.edges())
    assert all(after.has_edge(edge) for edge in before.edges())
    assert all(before.face_vertices(a) == after.face_vertices(b) for a, b in zip(before.faces(), after.faces()))
    assert before.guid == after.guid


def test_json_volmesh():
    before = VolMesh.from_vertices_and_cells(
        [
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 1, 1],
        ],
        [
            [
                [0, 1, 5, 4],
                [1, 2, 5, 6],
                [2, 3, 7, 6],
                [3, 0, 4, 7],
                [4, 5, 6, 7],
                [0, 3, 2, 1],
            ]
        ],
    )
    after = compas.json_loads(compas.json_dumps(before))
    assert before.dtype == after.dtype
    assert before.attributes == after.attributes
    assert all(before.has_vertex(vertex) for vertex in after.vertices())
    assert all(after.has_vertex(vertex) for vertex in before.vertices())
    # assert all(before.has_face(face) for face in after.faces())
    # assert all(after.has_face(face) for face in before.faces())
    # assert all(before.has_cell(cell) for cell in after.cells())
    # assert all(after.has_cell(cell) for cell in before.cells())
    # assert all(before.has_edge(edge) for edge in after.edges())
    # assert all(after.has_edge(edge) for edge in before.edges())
    assert before.guid == after.guid


def test_json_pretty():
    result = compas.json_dumps(dict(a=12, b=6565), pretty=True)
    # strip some spacing to make the test pass on ironpython
    result = "\n".join([line.strip() for line in result.split("\n")])
    assert result == """{\n"a": 12,\n"b": 6565\n}"""


# temporarily commented because folder does not exist yet on main
# def test_json_url():
#     data = compas.json_load('https://raw.githubusercontent.com/compas-dev/compas/main/src/compas/data/schemas/graph.json')
#     assert data['$schema'] == 'http://json-schema.org/draft-07/schema#'
