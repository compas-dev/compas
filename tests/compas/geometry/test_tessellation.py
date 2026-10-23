import numpy as np  # pyright: ignore[reportMissingImports]

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


def test_polygonal_geometry_produces_tessellations():
    polygon = Polygon([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    region = PlanarRegion([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    surface = PolygonalSurface([[0, 0, 0], [1, 0, 0], [0, 1, 0]], [[0, 1, 2]])
    polyhedron = Polyhedron.from_platonicsolid(4)

    assert polygon.tessellated().number_of_triangles == 1
    assert region.tessellated().number_of_triangles == 1
    assert surface.tessellated().vertices is surface.vertices
    assert polyhedron.tessellated().number_of_triangles == 4


def test_parametric_geometry_produces_tessellations():
    shape_tessellation = Box(1.0).tessellated()
    surface_tessellation = PlanarSurface().tessellated(nu=2, nv=3)

    assert shape_tessellation.number_of_triangles == 12
    assert surface_tessellation.number_of_vertices == 12
    assert surface_tessellation.number_of_triangles == 12


def test_surface_tessellation_aligns_positions_normals_uvs_and_winding():
    tessellation = PlanarSurface().tessellated(nu=2, nv=3)

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


def test_surface_tessellation_attributes_are_optional():
    tessellation = PlanarSurface().tessellated(
        include_normals=False,
        include_texture_coordinates=False,
    )

    assert tessellation.vertex_normals is None
    assert tessellation.texture_coordinates is None


def test_shape_tessellation_resolution_override_does_not_mutate_shape():
    shape = Sphere(1.0)
    original_u = shape.resolution_u
    original_v = shape.resolution_v

    tessellation = shape.tessellated(u=5, v=7)

    assert tessellation.number_of_vertices == 32
    assert shape.resolution_u == original_u
    assert shape.resolution_v == original_v


def test_direct_conversions_preserve_polygonal_topology():
    shape = Box(1.0)
    surface = PlanarSurface()
    polygonal_surface = PolygonalSurface(
        [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]],
        [[0, 1, 2, 3]],
    )

    assert shape.to_mesh().number_of_faces() == 6
    assert shape.tessellated().to_mesh().number_of_faces() == 12
    assert surface.to_mesh(nu=2, nv=3).number_of_faces() == 6
    assert surface.tessellated(nu=2, nv=3).to_mesh().number_of_faces() == 12
    assert polygonal_surface.to_mesh().number_of_faces() == 1
    assert polygonal_surface.tessellated().to_mesh().number_of_faces() == 2


def test_shape_topology_results_do_not_expose_cached_mutable_lists():
    shape = Box(1.0)
    _, faces = shape.to_vertices_and_faces()
    triangles = shape.tessellated().triangles

    faces[0][0] = 99

    assert shape.to_vertices_and_faces()[1][0][0] != 99
    assert isinstance(triangles, tuple)
    assert all(isinstance(triangle, tuple) for triangle in triangles)


def test_shape_polygonal_representation_is_cached_and_invalidated():
    shape = Box(1.0)

    vertices = shape.vertices
    edges = shape.edges
    faces = shape.faces

    assert shape.vertices is vertices
    assert shape.edges is edges
    assert shape.faces is faces
    assert len(shape.points) == len(vertices)
    assert len(shape.lines) == len(edges)
    assert len(shape.polygons) == len(faces)

    shape.resolution_u = 8
    assert shape.vertices is not vertices
    assert shape.edges is not edges
    assert shape.faces is not faces

    vertices = shape.vertices
    shape.xsize = 2.0
    assert shape.vertices is not vertices

    vertices = shape.vertices
    shape.frame.point.x = 1.0
    assert shape.vertices is not vertices


def test_surface_polygonal_representation_is_cached_and_invalidated():
    surface = PlanarSurface()

    vertices = surface.vertices
    edges = surface.edges
    faces = surface.faces

    assert surface.vertices is vertices
    assert surface.edges is edges
    assert surface.faces is faces
    assert len(surface.points) == len(vertices)
    assert len(surface.lines) == len(edges)
    assert len(surface.polygons) == len(faces)

    surface.resolution_u = 8
    assert surface.vertices is not vertices
    assert surface.edges is not edges
    assert surface.faces is not faces

    vertices = surface.vertices
    surface.xsize = 2.0
    assert surface.vertices is not vertices

    vertices = surface.vertices
    surface.frame.point.x = 1.0
    assert surface.vertices is not vertices
