import math

import numpy as np  # pyright: ignore[reportMissingImports]
import pytest

import compas
from compas.geometry import Adaptive
from compas.geometry import Box
from compas.geometry import Deflection
from compas.geometry import DiagonalSplit
from compas.geometry import EarClipping
from compas.geometry import FaceTriangulation
from compas.geometry import Native
from compas.geometry import PlanarRegion
from compas.geometry import PlanarSurface
from compas.geometry import Polygon
from compas.geometry import PolygonalSurface
from compas.geometry import Polyhedron
from compas.geometry import Sphere
from compas.geometry import Tessellation
from compas.geometry import TessellationStrategy
from compas.geometry import UGrid
from compas.geometry import UVGrid
from compas.geometry import normal_triangle
from compas.tolerance import TOL


@pytest.mark.parametrize(
    "strategy",
    [
        Native(),
        UGrid(8),
        UVGrid(8, 4),
        Deflection(0.01, 15.0),
        Adaptive(max_deviation=0.01),
        Adaptive(max_angle=5.0, max_edge_length=0.1),
    ],
)
def test_tessellation_strategies_are_data(strategy):
    assert isinstance(strategy, TessellationStrategy)
    other = compas.json_loads(compas.json_dumps(strategy))
    assert other == strategy
    assert hash(other) == hash(strategy)


def test_tessellation_strategies_are_immutable():
    strategy = UVGrid(8, 4)
    with pytest.raises(AttributeError):
        strategy.u = 16


@pytest.mark.parametrize("value", [0, -1, 1.5, True])
def test_grid_strategies_require_positive_integers(value):
    with pytest.raises((TypeError, ValueError)):
        UGrid(value)
    with pytest.raises((TypeError, ValueError)):
        UVGrid(1, value)


@pytest.mark.parametrize("value", [0.0, -1.0, math.inf, math.nan])
def test_deflection_requires_positive_finite_values(value):
    with pytest.raises(ValueError):
        Deflection(value, 1.0)
    with pytest.raises(ValueError):
        Deflection(1.0, value)


def test_deflection_uses_public_degrees():
    strategy = Deflection(0.01, 180.0)
    assert strategy.angular == 180.0
    with pytest.raises(ValueError):
        Deflection(0.01, 180.1)


def test_adaptive_requires_at_least_one_constraint():
    with pytest.raises(ValueError):
        Adaptive()
    with pytest.raises(ValueError):
        Adaptive(max_deviation=0.0)
    with pytest.raises(ValueError):
        Adaptive(max_angle=180.1)


def test_tessellation_retains_input_buffers():
    vertices = np.asarray([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    triangles = np.asarray([[0, 1, 2]])
    normals = np.asarray([[0.0, 0.0, 1.0]] * 3)
    texture_coordinates = np.asarray([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])

    tessellation = Tessellation(vertices, triangles, normals, texture_coordinates)

    assert tessellation.vertices is vertices
    assert tessellation.triangles is triangles
    assert tessellation.vertex_normals is normals
    assert tessellation.texture_coordinates is texture_coordinates
    result_vertices, result_triangles = tessellation.to_vertices_and_triangles()
    assert result_vertices is vertices
    assert result_triangles is triangles
    assert tessellation.number_of_vertices == 3
    assert tessellation.number_of_triangles == 1


def test_tessellation_converts_to_independent_compas_objects():
    vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    triangles = [[0, 1, 2]]
    tessellation = Tessellation(vertices, triangles)

    surface = tessellation.to_polygonal_surface()
    mesh = tessellation.to_mesh()
    vertices[0][0] = 10.0

    assert surface.vertices[0] == [0.0, 0.0, 0.0]
    assert mesh.vertex_coordinates(0) == [0.0, 0.0, 0.0]


@pytest.mark.parametrize(
    ("vertices", "triangles", "error"),
    [
        ([[0.0, 0.0]], [], ValueError),
        ([[0.0, 0.0, math.inf]], [], ValueError),
        ([[0.0, 0.0, 0.0]], [[0, 0]], ValueError),
        ([[0.0, 0.0, 0.0]], [[0, 0, 1]], IndexError),
        ([[0.0, 0.0, 0.0]], [[0, 0, 0.5]], TypeError),
    ],
)
def test_tessellation_validates_structural_buffers(vertices, triangles, error):
    with pytest.raises(error):
        Tessellation(vertices, triangles)


def test_tessellation_validates_aligned_attributes():
    vertices = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    triangles = [[0, 1, 2]]

    with pytest.raises(ValueError):
        Tessellation(vertices, triangles, vertex_normals=[[0.0, 0.0, 1.0]])
    with pytest.raises(ValueError):
        Tessellation(vertices, triangles, texture_coordinates=[[0.0, 0.0]])


def test_tessellation_validates_normal_coordinates():
    vertices = [[0.0, 0.0, 0.0]]

    with pytest.raises(ValueError):
        Tessellation(vertices, [], vertex_normals=[[0.0, 1.0]])
    with pytest.raises(TypeError):
        Tessellation(vertices, [], vertex_normals=[[0.0, 0.0, "up"]])


def test_tessellation_validates_texture_coordinates():
    vertices = [[0.0, 0.0, 0.0]]

    with pytest.raises(ValueError):
        Tessellation(vertices, [], texture_coordinates=[[0.0, 0.0, 1.0]])
    with pytest.raises(TypeError):
        Tessellation(vertices, [], texture_coordinates=[[0.0, "u"]])


def test_tessellation_validates_brep_style_polylines():
    vertices = [[0.0, 0.0, 0.0]]
    polylines = [
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
        [[1.0, 0.0, 0.0], [1.0, 1.0, 0.0]],
    ]

    tessellation = Tessellation(vertices, [], polylines=polylines)

    assert tessellation.polylines is polylines
    with pytest.raises(ValueError):
        Tessellation(vertices, [], polylines=[[[0.0, 0.0]]])
    with pytest.raises(ValueError):
        Tessellation(vertices, [], polylines=[[[0.0, 0.0, math.inf]]])


def test_tessellation_is_not_json_serializable():
    tessellation = Tessellation([[0.0, 0.0, 0.0]], [])

    with pytest.raises(TypeError, match="not JSON serializable"):
        compas.json_dumps(tessellation)


def test_polygonal_geometry_produces_tessellations():
    polygon = Polygon([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    region = PlanarRegion([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    surface = PolygonalSurface([[0, 0, 0], [1, 0, 0], [0, 1, 0]], [[0, 1, 2]])
    polyhedron = Polyhedron.from_platonicsolid(4)

    face_strategy = FaceTriangulation(quad=EarClipping(), ngon=EarClipping())
    assert polygon.triangulated(face_strategy).number_of_triangles == 1
    assert region.triangulated(EarClipping()).number_of_triangles == 1
    assert surface.triangulated(face_strategy).vertices is surface.vertices
    assert polyhedron.triangulated(face_strategy).number_of_triangles == 4


def test_parametric_geometry_produces_tessellations():
    shape_tessellation = Box(1.0).tessellate(Native())
    surface_tessellation = PlanarSurface().tessellate(UVGrid(2, 3))

    assert shape_tessellation.number_of_triangles == 12
    assert surface_tessellation.number_of_vertices == 12
    assert surface_tessellation.number_of_triangles == 12


def test_surface_tessellation_aligns_positions_normals_uvs_and_winding():
    tessellation = PlanarSurface().tessellate(UVGrid(2, 3))

    assert tessellation.vertex_normals is not None
    assert tessellation.texture_coordinates is not None
    assert len(tessellation.vertex_normals) == tessellation.number_of_vertices
    assert len(tessellation.texture_coordinates) == tessellation.number_of_vertices
    assert tessellation.texture_coordinates[0] == [0.0, 0.0]
    assert tessellation.texture_coordinates[1] == [0.0, 1.0 / 3.0]
    assert tessellation.texture_coordinates[4] == [0.5, 0.0]
    assert tessellation.texture_coordinates[-1] == [1.0, 1.0]

    triangle = tessellation.triangles[0]
    face_normal = normal_triangle([tessellation.vertices[index] for index in triangle])
    assert TOL.is_allclose(face_normal, tessellation.vertex_normals[triangle[0]])


def test_surface_tessellation_always_includes_aligned_attributes():
    tessellation = PlanarSurface().tessellate(UVGrid(2, 3))

    assert tessellation.vertex_normals is not None
    assert tessellation.texture_coordinates is not None
    assert len(tessellation.vertex_normals) == tessellation.number_of_vertices
    assert len(tessellation.texture_coordinates) == tessellation.number_of_vertices


def test_shape_tessellation_has_no_stored_resolution():
    shape = Sphere(1.0)

    tessellation = shape.tessellate(UVGrid(5, 7))

    assert tessellation.number_of_vertices == 32
    assert not hasattr(shape, "resolution_u")
    assert not hasattr(shape, "resolution_v")


def test_direct_conversions_preserve_polygonal_topology():
    shape = Box(1.0)
    surface = PlanarSurface()
    polygonal_surface = PolygonalSurface(
        [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]],
        [[0, 1, 2, 3]],
    )

    assert shape.polygonize(Native()).to_mesh().number_of_faces() == 6
    assert shape.tessellate(Native()).to_mesh().number_of_faces() == 12
    assert surface.polygonize(UVGrid(2, 3)).to_mesh().number_of_faces() == 6
    assert surface.tessellate(UVGrid(2, 3)).to_mesh().number_of_faces() == 12
    assert polygonal_surface.to_mesh().number_of_faces() == 1
    assert polygonal_surface.triangulated(FaceTriangulation()).to_mesh().number_of_faces() == 2


def test_shape_topology_results_are_independent():
    shape = Box(1.0)
    first = shape.polygonize(Native())
    second = shape.polygonize(Native())
    triangles = shape.tessellate(Native()).triangles

    first.faces[0][0] = 99

    assert second.faces[0][0] != 99
    assert isinstance(triangles, tuple)
    assert all(isinstance(triangle, tuple) for triangle in triangles)


def test_surface_direct_and_two_step_tessellation_are_geometrically_consistent():
    surface = PlanarSurface()
    strategy = UVGrid(2, 3)

    direct = surface.tessellate(strategy)
    two_step = surface.polygonize(strategy).triangulated(FaceTriangulation(quad=DiagonalSplit("02")))

    assert TOL.is_allclose(direct.vertices, two_step.vertices)
    assert direct.number_of_triangles == two_step.number_of_triangles


def test_surface_tessellation_and_polygonization_follow_placement():
    surface = PlanarSurface()
    strategy = UVGrid(2, 3)
    original = surface.tessellate(strategy)

    surface.frame.point.x += 2.0
    moved = surface.tessellate(strategy)
    polygonal = surface.polygonize(strategy)

    for before, after in zip(original.vertices, moved.vertices, strict=True):
        assert TOL.is_close(after[0] - before[0], 2.0)
    assert TOL.is_allclose(moved.vertices, polygonal.vertices)


def test_shape_has_no_cached_polygonal_representation():
    shape = Box(1.0)

    assert not hasattr(shape, "vertices")
    assert not hasattr(shape, "edges")
    assert not hasattr(shape, "faces")
    assert not hasattr(shape, "lines")
    assert not hasattr(shape, "polygons")
    assert not hasattr(shape, "to_vertices_and_faces")
    assert not hasattr(shape, "compute_vertices")
    assert not hasattr(shape, "compute_edges")
    assert not hasattr(shape, "compute_faces")
    assert len(shape.points) == 8


def test_surface_has_no_cached_polygonal_representation():
    surface = PlanarSurface()

    assert not hasattr(surface, "vertices")
    assert not hasattr(surface, "edges")
    assert not hasattr(surface, "faces")
    assert not hasattr(surface, "points")
    assert not hasattr(surface, "lines")
    assert not hasattr(surface, "polygons")
