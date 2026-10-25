import json

import pytest

from compas.geometry import Box
from compas.geometry import PlanarSurface
from compas.geometry import PolygonalSurface
from compas.geometry import Translation


@pytest.fixture
def quad():
    return PolygonalSurface(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
        [[0, 1, 2, 3]],
    )


@pytest.fixture
def tetrahedron():
    return PolygonalSurface(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        [[0, 2, 1], [0, 1, 3], [1, 2, 3], [2, 0, 3]],
    )


def test_polygonal_surface_copies_input():
    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    faces = [[0, 1, 2]]
    surface = PolygonalSurface(vertices, faces)

    vertices[0][0] = 10
    faces[0][0] = 2

    assert surface.vertices[0] == [0.0, 0.0, 0.0]
    assert surface.faces[0] == [0, 1, 2]


def test_polygonal_surface_data_roundtrip(quad):
    data = json.loads(json.dumps(quad.__data__))
    reconstructed = PolygonalSurface.__from_data__(data)

    assert reconstructed.vertices == quad.vertices
    assert reconstructed.faces == quad.faces


def test_polygonal_surface_validates_vertices_and_faces():
    with pytest.raises(ValueError):
        PolygonalSurface([[0.0, 0.0]], [])
    with pytest.raises(TypeError):
        PolygonalSurface([["0", 0.0, 0.0]], [])
    with pytest.raises(ValueError):
        PolygonalSurface([[0.0, 0.0, 0.0]], [[0, 0, 0]])
    with pytest.raises(IndexError):
        PolygonalSurface([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], [[0, 1, 3]])


def test_polygonal_surface_geometry(quad):
    assert quad.area() == pytest.approx(1.0)
    assert len(quad.edges) == 4
    assert len(quad.points) == 4
    assert len(quad.lines) == 4
    assert len(quad.polygons) == 1
    assert not quad.is_closed
    assert quad.is_manifold
    assert quad.is_orientable


def test_closed_polygonal_surface(tetrahedron):
    assert tetrahedron.is_closed
    assert tetrahedron.is_manifold
    assert tetrahedron.is_orientable


def test_nonmanifold_polygonal_surface():
    surface = PolygonalSurface(
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1]],
        [[0, 1, 2], [1, 0, 3], [0, 1, 4]],
    )

    assert not surface.is_manifold
    assert not surface.is_orientable


def test_polygonal_surface_transform_invalidates_bounds(quad):
    initial = quad.aabb
    quad.transform(Translation.from_vector([2.0, 3.0, 4.0]))

    assert quad.aabb is not initial
    assert quad.vertices[0] == [2.0, 3.0, 4.0]


def test_polygonal_surface_conversions(quad):
    vertices, faces = quad.to_vertices_and_faces()
    vertices[0][0] = 10.0
    faces[0][0] = 2

    assert quad.vertices[0][0] == 0.0
    assert quad.faces[0][0] == 0

    reconstructed = PolygonalSurface.from_mesh(quad.to_mesh())
    assert reconstructed.vertices == quad.vertices
    assert reconstructed.faces == quad.faces


def test_shape_to_polygonal_surface():
    surface = Box(1.0).to_polygonal_surface()

    assert isinstance(surface, PolygonalSurface)
    assert surface.is_closed
    assert len(surface.faces) == 6


def test_parametric_surface_to_polygonal_surface():
    surface = PlanarSurface().to_polygonal_surface(nu=2, nv=3)

    assert isinstance(surface, PolygonalSurface)
    assert not surface.is_closed
    assert len(surface.vertices) == 12
    assert len(surface.faces) == 6


def test_polygonal_surface_triangulates_concave_faces():
    surface = PolygonalSurface(
        [[0, 0, 0], [2, 0, 0], [2, 1, 0], [1, 1, 0], [1, 2, 0], [0, 2, 0]],
        [[0, 1, 2, 3, 4, 5]],
    )
    vertices, triangles = surface.to_vertices_and_faces(triangulated=True)
    triangulated = PolygonalSurface(vertices, triangles)

    assert len(triangles) == 4
    assert all(len(triangle) == 3 for triangle in triangles)
    assert triangulated.area() == pytest.approx(surface.area())
