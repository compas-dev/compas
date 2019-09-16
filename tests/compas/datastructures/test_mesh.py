import pytest

import compas

import json

from compas.datastructures import Mesh

# --------------------------------------------------------------------------
# constructors
# --------------------------------------------------------------------------


@pytest.fixture
def polylines():
    boundary_polylines = [
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
        [[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
        [[2.0, 0.0, 0.0], [2.0, 1.0, 0.0]],
        [[2.0, 1.0, 0.0], [1.0, 1.0, 0.0]],
        [[1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
        [[0.0, 1.0, 0.0], [0.0, 0.0, 0.0]],
    ]
    other_polylines = [
        [[1.0, 0.0, 0.0], [1.0, 0.25, 0.0], [1.0, 0.5, 0.0], [1.0, 0.75, 0.0], [1.0, 1.0, 0.0]]
    ]

    return boundary_polylines, other_polylines


def test_from_polylines(polylines):
    boundary_polylines, other_polylines = polylines
    mesh = Mesh.from_polylines(boundary_polylines, other_polylines)
    assert mesh.number_of_vertices() == 6
    assert mesh.number_of_faces() == 2
    assert mesh.number_of_edges() == 7


def test_from_obj():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    assert mesh.number_of_faces() == 25
    assert mesh.number_of_vertices() == 36
    assert mesh.number_of_edges() == 60


def test_from_ply():
    mesh = Mesh.from_ply(compas.get('bunny.ply'))
    assert mesh.number_of_faces() == 69451
    assert mesh.number_of_vertices() == 35947
    assert mesh.number_of_edges() == 104288


def test_from_stl():
    mesh = Mesh.from_stl(compas.get('cube_ascii.stl'))
    assert mesh.number_of_faces() == 8016
    assert mesh.number_of_vertices() == 4020
    assert mesh.number_of_edges() == 11368

    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    assert mesh.number_of_faces() == 12
    assert mesh.number_of_vertices() == 8
    assert mesh.number_of_edges() == 18


def test_from_off():
    mesh = Mesh.from_off(compas.get('cube.off'))
    assert mesh.number_of_faces() == 6
    assert mesh.number_of_vertices() == 8
    assert mesh.number_of_edges() == 12


def test_from_lines():
    with open(compas.get('lines.json'), 'r') as fo:
        lines = json.load(fo)
    mesh = Mesh.from_lines(lines)
    assert mesh.number_of_faces() == 10
    assert mesh.number_of_vertices() == 32
    assert mesh.number_of_edges() == 40


def test_from_vertices_and_faces():
    # tested through other functions
    pass


def test_from_polyhedron():
    mesh = Mesh.from_polyhedron(8)
    assert mesh.number_of_faces() == 8
    assert mesh.number_of_vertices() == 6
    assert mesh.number_of_edges() == 12


def test_from_points():
    points = [[1.0, 0.0, 3.0], [1.0, 1.25, 0.0], [1.5, 0.5, 0.0], [1.0, 10.75, 0.2], [1.0, 1.0, 4.0]]
    mesh = Mesh.from_points(points)
    assert mesh.number_of_faces() == 3
    assert mesh.number_of_vertices() == 5
    assert mesh.number_of_edges() == 7
    # TODO: add test for boundary and holes


def test_from_ploygons():
    polygon = [[[1.0, 0.0, 3.0], [1.0, 1.25, 0.0], [1.5, 0.5, 0.0]], [[1.0, 0.0, 3.0], [1.0, 5.25, 0.0], [1.5, 0.5, 0.0]]]
    mesh = Mesh.from_polygons(polygon)
    assert mesh.number_of_faces() == 2
    assert mesh.number_of_vertices() == 4
    assert mesh.number_of_edges() == 5


# --------------------------------------------------------------------------
# converters
# --------------------------------------------------------------------------

def test_to_obj():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    mesh.to_obj('data/temp.obj')
    mesh = Mesh.from_obj(compas.get('temp.obj'))
    assert mesh.number_of_faces() == 25
    assert mesh.number_of_vertices() == 36
    assert mesh.number_of_edges() == 60


def test_to_vertices_and_faces():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    vertices, faces = mesh.to_vertices_and_faces()
    assert len(vertices) == 36
    assert len(faces) == 25


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def test_copy():
    mesh1 = Mesh.from_obj(compas.get('faces.obj'))
    mesh2 = mesh1.copy()
    assert mesh1.number_of_faces() == mesh2.number_of_faces()
    assert mesh1.number_of_vertices() == mesh2.number_of_vertices()
    assert mesh1.number_of_edges() == mesh2.number_of_edges()


def test_clear():
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    mesh.clear()
    assert mesh.number_of_faces() == 0
    assert mesh.number_of_vertices() == 0
    assert mesh.number_of_edges() == 0


def test_clear_vertexdict():
    pass


def test_clear_facedict():
    pass


def test_clear_halfedgedict():
    pass


# --------------------------------------------------------------------------
# builders
# --------------------------------------------------------------------------

def test_add_vertex():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    n = mesh.number_of_vertices()
    key = mesh.add_vertex(x=0, y=1, z=2)
    assert mesh.vertex[key] == {'x': 0, 'y': 1, 'z': 2}
    assert mesh.number_of_vertices() == n+1


def test_add_face():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    n = mesh.number_of_faces()
    key = mesh.add_face([0, 1, 2])
    assert mesh.face[key] == [0, 1, 2]
    assert mesh.number_of_faces() == n+1


# --------------------------------------------------------------------------
# modifiers
# --------------------------------------------------------------------------

def test_delete_vertex():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    n = mesh.number_of_vertices()
    fn = mesh.number_of_faces()
    en = mesh.number_of_edges()
    mesh.delete_vertex(0)
    assert mesh.number_of_vertices() == n-1
    assert mesh.number_of_faces() == fn-4
    assert mesh.number_of_edges() == en-4


def test_insert_vertex():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    n = mesh.number_of_vertices()
    fn = mesh.number_of_faces()
    en = mesh.number_of_edges()
    mesh.insert_vertex(0)
    assert mesh.number_of_vertices() == n + 1
    assert mesh.number_of_faces() == fn + 2
    assert mesh.number_of_edges() == en + 3


def test_delete_face():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    fn = mesh.number_of_faces()
    mesh.delete_face(0)
    assert mesh.number_of_faces() == fn-1


def test_cull_vertices():
    mesh = Mesh.from_stl(compas.get('cube_binary.stl'))
    mesh.add_vertex()
    n = mesh.number_of_vertices()
    mesh.cull_vertices()
    assert mesh.number_of_vertices() == n - 1


def test_cull_edges():
    # TODO: to be updated
    pass
