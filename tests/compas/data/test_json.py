import os
import tempfile

import compas
from compas.datastructures import Mesh
from compas.datastructures import Graph
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
    after = compas.json_loads(compas.json_dumps(before))  # type: Point
    assert before.__dtype__ == after.__dtype__
    assert all(a == b for a, b in zip(before, after))
    assert before.guid == after.guid


def test_json_shape():
    before = Box(frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0)), xsize=1, ysize=1, zsize=1)
    after = compas.json_loads(compas.json_dumps(before))  # type: Box
    assert before.__dtype__ == after.__dtype__
    assert all(a == b for a, b in zip(before.to_vertices_and_faces()[0], after.to_vertices_and_faces()[0]))
    assert before.guid == after.guid


def test_json_xform():
    before = Transformation.from_frame_to_frame(Frame.worldXY(), Frame.worldXY())
    after = compas.json_loads(compas.json_dumps(before))  # type: Transformation
    assert before.__dtype__ == after.__dtype__
    assert all(a == b for a, b in zip(before, after))
    assert before.guid == after.guid


def test_json_graph():
    before = Graph()
    a = before.add_node()
    b = before.add_node()
    before.add_edge(a, b)
    after = compas.json_loads(compas.json_dumps(before))  # type: Graph
    assert before.__dtype__ == after.__dtype__
    # assert before.attributes == after.attributes
    assert all(before.has_node(node) for node in after.nodes())
    assert all(after.has_node(node) for node in before.nodes())
    assert all(before.has_edge(edge) for edge in after.edges())
    assert all(after.has_edge(edge) for edge in before.edges())
    assert before.guid == after.guid


def test_json_mesh():
    before = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
    after = compas.json_loads(compas.json_dumps(before))  # type: Mesh
    assert before.__dtype__ == after.__dtype__
    # assert before.attributes == after.attributes
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
    after = compas.json_loads(compas.json_dumps(before))  # type: VolMesh
    assert before.__dtype__ == after.__dtype__
    # assert before.attributes == after.attributes
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


def test_json_zip():
    zipfile_name = os.path.join(tempfile.gettempdir(), "test.json.zip")

    before = Box(frame=Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0)), xsize=2, ysize=5, zsize=3)
    compas.json_dumpz(before, zipfile_name)
    after = compas.json_loadz(zipfile_name)  # type: Box
    assert before.__dtype__ == after.__dtype__
    assert all(a == b for a, b in zip(before.to_vertices_and_faces()[0], after.to_vertices_and_faces()[0]))
    assert before.guid == after.guid


def test_json_attributeview():
    mesh = Mesh.from_meshgrid(10, 10)
    before = Mesh()
    for vertex in mesh.vertices():
        attr = mesh.vertex_attributes(vertex)
        before.add_vertex(key=vertex, attr_dict=attr)
    for face in mesh.faces():
        attr = mesh.face_attributes(face)
        before.add_face(vertices=mesh.face_vertices(face), fkey=face, attr_dict=attr)
    after = compas.json_loads(compas.json_dumps(before))  # type: Mesh

    assert before.__dtype__ == after.__dtype__
    assert all(before.has_vertex(vertex) for vertex in after.vertices())
    assert all(after.has_vertex(vertex) for vertex in before.vertices())
    assert all(before.has_face(face) for face in after.faces())
    assert all(after.has_face(face) for face in before.faces())
    assert all(before.has_edge(edge) for edge in after.edges())
    assert all(after.has_edge(edge) for edge in before.edges())
    assert all(before.face_vertices(a) == after.face_vertices(b) for a, b in zip(before.faces(), after.faces()))
    assert before.guid == after.guid


# temporarily commented because folder does not exist yet on main
# def test_json_url():
#     data = compas.json_load('https://raw.githubusercontent.com/compas-dev/compas/main/src/compas/data/schemas/graph.json')
#     assert data['$schema'] == 'http://json-schema.org/draft-07/schema#'
