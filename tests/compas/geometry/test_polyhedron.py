from compas.geometry import Polyhedron
from compas.geometry import Point
from compas.itertools import pairwise


def test_polyhedron():
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    faces = [[0, 1, 2, 3]]
    name = "Test Polyhedron"
    polyhedron = Polyhedron(vertices, faces, name)

    assert polyhedron.vertices == vertices
    assert polyhedron.faces == faces
    assert polyhedron.name == name
    assert all(u < len(polyhedron.vertices) and v < len(polyhedron.vertices) for u, v in polyhedron.edges)
    assert all(v < len(polyhedron.vertices) for face in polyhedron.faces for v in face)
    assert polyhedron.points == vertices
    assert polyhedron.lines == [(a, b) for a, b in pairwise(vertices[-1:] + vertices)]
    assert polyhedron.points[0] == vertices[0]
    assert polyhedron.points[-1] != polyhedron.points[0]


def test_polyhedron_vertices():
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    faces = [[0, 1, 2, 3]]
    name = "Test Polyhedron"
    polyhedron = Polyhedron(vertices, faces, name)

    polyhedron_vertices = polyhedron.vertices
    assert all(isinstance(vertex, list) and len(vertex) == 3 for vertex in polyhedron_vertices)

    vertices = [Point(0, 0, 0), Point(1, 0, 0), Point(1, 1, 0), Point(0, 1, 0)]
    polyhedron = Polyhedron(vertices, faces, name)
    polyhedron_vertices = polyhedron.vertices
    assert all(isinstance(vertex, list) and len(vertex) == 3 for vertex in polyhedron_vertices)
