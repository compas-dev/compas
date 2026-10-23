import json

import pytest

from compas.geometry import Point
from compas.geometry import PolygonalSurface
from compas.geometry import Polyhedron
from compas.geometry import Scale


def test_polygonal_surface_geometric_views():
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    faces = [[0, 1, 2, 3]]
    name = "Test Polyhedron"
    surface = PolygonalSurface(vertices, faces, name)

    assert surface.vertices == vertices
    assert surface.faces == faces
    assert surface.name == name
    assert all(u < len(surface.vertices) and v < len(surface.vertices) for u, v in surface.edges)
    assert all(v < len(surface.vertices) for face in surface.faces for v in face)
    assert surface.points == vertices
    assert surface.lines == [(vertices[u], vertices[v]) for u, v in surface.edges]
    assert surface.points[0] == vertices[0]
    assert surface.points[-1] != surface.points[0]


def test_polyhedron_is_closed_solid():
    polyhedron = Polyhedron.from_platonicsolid(4)

    assert isinstance(polyhedron.boundary, PolygonalSurface)
    assert polyhedron.is_closed
    assert polyhedron.boundary.is_manifold
    assert polyhedron.boundary.is_oriented
    assert polyhedron.volume() > 0.0
    assert polyhedron.centroid() == Point(0.0, 0.0, 0.0)


def test_polyhedron_data_roundtrip():
    polyhedron = Polyhedron.from_platonicsolid(6)
    data = json.loads(json.dumps(polyhedron.__data__))
    reconstructed = Polyhedron.__from_data__(data)

    assert reconstructed.vertices == polyhedron.vertices
    assert reconstructed.faces == polyhedron.faces
    assert reconstructed.volume() == pytest.approx(polyhedron.volume())


def test_polyhedron_rejects_open_boundary():
    with pytest.raises(ValueError, match="closed"):
        Polyhedron([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])


def test_polyhedron_rejects_inconsistently_oriented_boundary():
    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
    faces = [[0, 2, 1], [0, 1, 3], [1, 2, 3], [0, 2, 3]]

    with pytest.raises(ValueError, match="oriented"):
        Polyhedron(vertices, faces)


def test_polyhedron_normalizes_inward_orientation():
    outward = Polyhedron.from_platonicsolid(4)
    inward = Polyhedron(outward.vertices, [face[::-1] for face in outward.faces])

    assert inward.volume() == pytest.approx(outward.volume())
    assert inward.volume() > 0.0


def test_polyhedron_transform_updates_cached_volume():
    polyhedron = Polyhedron.from_platonicsolid(6)
    initial = polyhedron.volume()
    polyhedron.transform(Scale.from_factors([2.0, 3.0, 4.0]))

    assert polyhedron.volume() == pytest.approx(initial * 24.0)


def test_polyhedron_rejects_collapsing_transform_without_mutation():
    polyhedron = Polyhedron.from_platonicsolid(6)
    vertices = polyhedron.vertices

    with pytest.raises(ValueError, match="collapse"):
        polyhedron.transform(Scale.from_factors([1.0, 1.0, 0.0]))

    assert polyhedron.vertices == vertices


def test_polyhedron_triangulates_polygonal_boundary():
    polyhedron = Polyhedron.from_platonicsolid(6)
    vertices, faces = polyhedron.to_vertices_and_faces(triangulated=True)

    assert len(vertices) == 8
    assert len(faces) == 12
    assert all(len(face) == 3 for face in faces)


def test_polyhedron_boolean_receives_triangles(monkeypatch):
    captured = []

    def boolean_union(A, B):
        captured.extend([A, B])
        return A

    monkeypatch.setattr("compas.geometry.boolean_union_mesh_mesh", boolean_union)
    polyhedron = Polyhedron.from_platonicsolid(6)
    result = polyhedron.boolean_union(polyhedron)

    assert isinstance(result, Polyhedron)
    assert all(len(face) == 3 for _, faces in captured for face in faces)
