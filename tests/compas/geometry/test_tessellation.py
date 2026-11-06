import math
from operator import index

import numpy as np  # pyright: ignore[reportMissingImports]
import pytest

import compas
from compas.geometry import Box
from compas.geometry import PlanarRegion
from compas.geometry import PlanarSurface
from compas.geometry import Polygon
from compas.geometry import PolygonalSurface
from compas.geometry import Polyhedron
from compas.geometry import Sphere
from compas.geometry import Tessellation
from compas.geometry import normal_triangle
from compas.tolerance import TOL


class FloatLike:
    def __init__(self, value):
        self.value = value
        self.conversions = 0

    def __float__(self):
        self.conversions += 1
        return float(self.value)


class IndexLike:
    def __init__(self, value):
        self.value = value
        self.conversions = 0

    def __index__(self):
        self.conversions += 1
        return index(self.value)


class DuckBuffer:
    def __init__(self, values):
        self.values = values

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __iter__(self):
        return iter(self.values)


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


def test_tessellation_retains_noncontiguous_readonly_buffers_without_mutation():
    vertex_source = np.arange(18.0).reshape(3, 6)
    vertices = vertex_source[:, ::2]
    vertices.setflags(write=False)
    triangles = np.asfortranarray([[0, 1, 2]], dtype=np.int32)
    normals = np.asfortranarray([[0.0, 0.0, 1.0]] * 3)
    texture_coordinates = np.arange(12.0).reshape(3, 4)[:, ::2]
    texture_coordinates.setflags(write=False)
    polylines = np.asfortranarray([[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]])
    before = vertex_source.copy(), triangles.copy(), normals.copy(), texture_coordinates.copy(), polylines.copy()

    tessellation = Tessellation(vertices, triangles, normals, texture_coordinates, polylines)

    assert tessellation.vertices is vertices
    assert tessellation.triangles is triangles
    assert tessellation.vertex_normals is normals
    assert tessellation.texture_coordinates is texture_coordinates
    assert tessellation.polylines is polylines
    for actual, expected in zip((vertex_source, triangles, normals, texture_coordinates, polylines), before):
        np.testing.assert_array_equal(actual, expected)


def test_tessellation_validates_duck_typed_numeric_elements_by_capability():
    vertices = DuckBuffer([DuckBuffer([FloatLike(0.0), FloatLike(0.0), FloatLike(0.0)])])
    triangles = DuckBuffer([DuckBuffer([IndexLike(0), IndexLike(0), IndexLike(0)])])

    tessellation = Tessellation(vertices, triangles)

    assert tessellation.vertices is vertices
    assert tessellation.triangles is triangles


@pytest.mark.parametrize("value", [True, np.bool_(True)])
def test_tessellation_rejects_boolean_coordinate_elements(value):
    with pytest.raises(TypeError, match="coordinates should be real numbers"):
        Tessellation([[value, 0.0, 0.0]], [])


@pytest.mark.parametrize("value", [True, np.bool_(True)])
def test_tessellation_rejects_boolean_index_elements(value):
    with pytest.raises(TypeError, match="indices should be integers"):
        Tessellation([[0.0, 0.0, 0.0]], [[value, 0, 0]])


@pytest.mark.parametrize("conversion", ["surface", "mesh"])
def test_tessellation_normalizes_once_only_at_materialization_boundaries(conversion):
    coordinate_values = [
        FloatLike(0.0),
        FloatLike(0.0),
        FloatLike(0.0),
        FloatLike(1.0),
        FloatLike(0.0),
        FloatLike(0.0),
        FloatLike(0.0),
        FloatLike(1.0),
        FloatLike(0.0),
    ]
    index_values = [IndexLike(0), IndexLike(1), IndexLike(2)]
    vertices = DuckBuffer([DuckBuffer(coordinate_values[offset : offset + 3]) for offset in range(0, 9, 3)])
    triangles = DuckBuffer([DuckBuffer(index_values)])
    tessellation = Tessellation(vertices, triangles)
    for value in coordinate_values + index_values:
        value.conversions = 0

    if conversion == "surface":
        result = tessellation.to_polygonal_surface()
        assert result.vertices == [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        assert result.faces == [[0, 1, 2]]
    else:
        result = tessellation.to_mesh()
        assert result.vertex_coordinates(0) == [0.0, 0.0, 0.0]
        assert result.face_vertices(0) == [0, 1, 2]

    assert tessellation.vertices is vertices
    assert tessellation.triangles is triangles
    assert all(value.conversions == 1 for value in coordinate_values + index_values)


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


def test_tessellation_does_not_mutate_buffers_when_validation_fails():
    vertices = np.asarray([[0.0, 0.0, 0.0]])
    triangles = np.asarray([[0, 0, 1]], dtype=np.int64)
    vertices_before = vertices.copy()
    triangles_before = triangles.copy()

    with pytest.raises(IndexError, match="triangle index is out of range"):
        Tessellation(vertices, triangles)

    np.testing.assert_array_equal(vertices, vertices_before)
    np.testing.assert_array_equal(triangles, triangles_before)


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

    assert polygon.triangulated().number_of_triangles == 1
    assert region.triangulated().number_of_triangles == 1
    assert surface.triangulated().vertices is surface.vertices
    assert polyhedron.triangulated().number_of_triangles == 4


def test_parametric_geometry_produces_tessellations():
    shape_tessellation = Box(1.0).to_tessellation()
    surface_tessellation = PlanarSurface().to_tessellation(nu=2, nv=3)

    assert shape_tessellation.number_of_triangles == 12
    assert surface_tessellation.number_of_vertices == 12
    assert surface_tessellation.number_of_triangles == 12


def test_surface_tessellation_aligns_positions_normals_uvs_and_winding():
    tessellation = PlanarSurface().to_tessellation(nu=2, nv=3)

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
    tessellation = PlanarSurface().to_tessellation(nu=2, nv=3)

    assert tessellation.vertex_normals is not None
    assert tessellation.texture_coordinates is not None
    assert len(tessellation.vertex_normals) == tessellation.number_of_vertices
    assert len(tessellation.texture_coordinates) == tessellation.number_of_vertices


def test_shape_tessellation_has_no_stored_resolution():
    shape = Sphere(1.0)

    tessellation = shape.to_tessellation(nu=5, nv=7)

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

    assert shape.to_polygonal_surface().to_mesh().number_of_faces() == 6
    assert shape.to_tessellation().to_mesh().number_of_faces() == 12
    assert surface.to_polygonal_surface(nu=2, nv=3).to_mesh().number_of_faces() == 6
    assert surface.to_tessellation(nu=2, nv=3).to_mesh().number_of_faces() == 12
    assert polygonal_surface.to_mesh().number_of_faces() == 1
    assert polygonal_surface.triangulated().to_mesh().number_of_faces() == 2


def test_shape_topology_results_are_independent():
    shape = Box(1.0)
    first = shape.to_polygonal_surface()
    second = shape.to_polygonal_surface()
    triangles = shape.to_tessellation().triangles

    first.faces[0][0] = 99

    assert second.faces[0][0] != 99
    assert isinstance(triangles, list)
    assert all(isinstance(triangle, list) for triangle in triangles)


def test_surface_direct_and_two_step_tessellation_are_geometrically_consistent():
    surface = PlanarSurface()
    direct = surface.to_tessellation(nu=2, nv=3)
    two_step = surface.to_polygonal_surface(nu=2, nv=3).triangulated()

    assert TOL.is_allclose(direct.vertices, two_step.vertices)
    assert direct.number_of_triangles == two_step.number_of_triangles


def test_surface_tessellation_and_polygonization_follow_placement():
    surface = PlanarSurface()
    original = surface.to_tessellation(nu=2, nv=3)

    surface.frame.point.x += 2.0
    moved = surface.to_tessellation(nu=2, nv=3)
    polygonal = surface.to_polygonal_surface(nu=2, nv=3)

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
