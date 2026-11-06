from functools import partial

import numpy as np
import pytest

import compas.geometry as geometry
from compas.datastructures import Mesh
from compas.geometry import PolygonalSurface
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import triangulate_polygon
from compas.geometry import triangulate_polygon_earclip
from compas.geometry import triangulate_polygon_minimum_area
from compas.geometry import triangulate_polygon_projected
from compas.geometry import triangulate_quadrilateral


PENTAGON = [[0, 0, 0], [2, 0, 0], [3, 1, 0], [1.5, 2, 0], [0, 1, 0]]
DEGENERATE_PENTAGON = [[0, 0, 0], [1, 0, 0], [2, 0, 0], [2, 1, 0], [0, 1, 0]]


def make_single_face_geometry(kind, vertices):
    face = list(range(len(vertices)))
    if kind == "polygon":
        return Polygon(vertices)
    if kind == "surface":
        return PolygonalSurface(vertices, [face])
    if kind == "polyhedron":
        apex = [sum(vertex[0] for vertex in vertices) / len(vertices), 1.0, 3.0]
        faces = [face]
        apex_index = len(vertices)
        faces.extend([[(index + 1) % len(vertices), index, apex_index] for index in range(len(vertices))])
        return Polyhedron([*vertices, apex], faces)
    return Mesh.from_vertices_and_faces(vertices, [face])


def invalid_triangulation(failure, vertex_count):
    valid = [[0, index, index + 1] for index in range(1, vertex_count - 1)]
    if failure == "incomplete":
        return valid[:-1]
    if failure == "duplicate":
        return [valid[0], valid[0], *valid[2:]]
    if failure == "reversed":
        return [[a, c, b] for a, b, c in valid]
    if failure == "invalid-incidence":
        if vertex_count == 4:
            return [[0, 1, 3], [0, 2, 3]]
        return [[0, 1, 3], [1, 2, 4], [2, 3, 4]]
    if failure == "degenerate" and vertex_count == 5:
        return [[2, 3, 4], [0, 1, 2], [0, 2, 4]]
    return valid


def triangulation_faces(result):
    if isinstance(result, Mesh):
        return result.to_vertices_and_faces()[1]
    return result.triangles


def test_removed_strategy_types_are_not_public():
    for name in (
        "TriangulationStrategy",
        "FaceTriangulation",
        "DiagonalSplit",
        "EarClipping",
        "ProjectedEarClipping",
        "MinimumAreaTriangulation",
    ):
        assert not hasattr(geometry, name)


def test_named_quadrilateral_triangulation():
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    assert triangulate_quadrilateral(vertices, diagonal="02") == [[0, 1, 2], [0, 2, 3]]
    assert triangulate_quadrilateral(vertices, diagonal="13") == [[0, 1, 3], [1, 2, 3]]
    assert triangulate_polygon(vertices) == [[0, 1, 2], [0, 2, 3]]


def test_quadrilateral_shortest_uses_only_valid_interior_diagonals():
    concave = [[0, 100, 0], [-1, 0, 0], [0, 0.1, 0], [1, 0, 0]]

    triangles = triangulate_quadrilateral(concave)
    assert triangles == [[0, 1, 2], [0, 2, 3]]
    assert triangulate_polygon(concave) == [[0, 1, 2], [0, 2, 3]]
    assert triangulate_quadrilateral(concave, diagonal="02") == triangles

    reversed_concave = list(reversed(concave))
    reversed_triangles = triangulate_quadrilateral(reversed_concave)
    assert reversed_triangles == [[0, 1, 3], [1, 2, 3]]

    def signed_area(points):
        return sum(point[0] * next_point[1] - next_point[0] * point[1] for point, next_point in zip(points, points[1:] + points[:1]))

    for boundary, result in ((concave, triangles), (reversed_concave, reversed_triangles)):
        boundary_area = signed_area(boundary)
        assert all(signed_area([boundary[index] for index in triangle]) * boundary_area > 0 for triangle in result)

    with pytest.raises(ValueError, match="outside"):
        triangulate_quadrilateral(concave, diagonal="13")


@pytest.mark.parametrize("triangulator", [triangulate_quadrilateral, triangulate_polygon])
def test_polygon_triangulation_rejects_self_intersecting_quadrilateral_boundary(triangulator):
    bow_tie = [[0, 0, 0], [1, 1, 0], [0, 1, 0], [1, 0, 0]]
    with pytest.raises(ValueError, match="self-intersect"):
        triangulator(bow_tie)


def test_quadrilateral_triangulation_accepts_warped_simple_boundary():
    warped = [[0, 0, 0], [1, 0, 0], [1, 1, 1], [0, 1, 0]]
    assert triangulate_quadrilateral(warped, diagonal="02") == [[0, 1, 2], [0, 2, 3]]


def test_triangulation_coincidence_checks_are_independent_of_coordinate_scale():
    offset = 1_000_000.0
    vertices = [
        [offset, offset, offset],
        [offset + 1, offset, offset],
        [offset + 1, offset + 1, offset],
        [offset, offset + 1, offset],
    ]
    assert triangulate_polygon(vertices) == [[0, 1, 2], [0, 2, 3]]


@pytest.mark.parametrize("dtype", [np.float32, np.float64, np.int32, np.int64])
@pytest.mark.parametrize("layout", ["c", "f", "sliced", "readonly"])
def test_triangulate_polygon_accepts_numpy_inputs_without_mutation(dtype, layout):
    values = np.asarray([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], dtype=dtype)
    if layout == "f":
        vertices = np.asfortranarray(values)
    elif layout == "sliced":
        vertices = np.pad(values, ((0, 0), (0, 1)))[:, :3]
    else:
        vertices = values.copy()
    if layout == "readonly":
        vertices.flags.writeable = False
    before = vertices.copy()

    assert triangulate_quadrilateral(vertices, diagonal="02") == [[0, 1, 2], [0, 2, 3]]
    np.testing.assert_array_equal(vertices, before)


def test_named_polygon_algorithms():
    polygon = [[0, 0, 0], [2, 0, 0], [2, 2, 0], [1, 1, 0], [0, 2, 0]]
    assert len(triangulate_polygon_earclip(polygon)) == 3
    assert len(triangulate_polygon_projected(polygon, max_deviation=0.1)) == 3
    assert len(triangulate_polygon_minimum_area(polygon)) == 3


def test_projected_triangulation_requires_positive_finite_bound():
    polygon = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
    with pytest.raises(TypeError):
        triangulate_polygon_projected(polygon, max_deviation=True)
    with pytest.raises(ValueError):
        triangulate_polygon_projected(polygon, max_deviation=0.0)


def test_aggregate_triangulation_accepts_callable_and_maps_indices():
    surface = PolygonalSurface(
        [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]],
        [[0, 1, 2, 3]],
    )
    result = surface.triangulated(partial(triangulate_quadrilateral, diagonal="13"))
    assert result.triangles == [[0, 1, 3], [1, 2, 3]]


@pytest.mark.parametrize(
    ("triangle", "exception"),
    [
        ([0, 1], ValueError),
        ([-1, 1, 2], ValueError),
        ([0, 1, 4], ValueError),
        ([0, 0, 1], ValueError),
        ([0, 1, 2.0], TypeError),
    ],
)
@pytest.mark.parametrize(
    "geometry",
    [
        Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]),
        PolygonalSurface([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]]),
        Polyhedron.from_platonicsolid(6),
        Mesh.from_polyhedron(6),
    ],
)
def test_aggregate_triangulation_validates_callable_results(geometry, triangle, exception):
    with pytest.raises(exception):
        geometry.triangulated(lambda vertices: [triangle])


def test_aggregate_triangulation_accepts_supports_index_results():
    polygon = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
    tessellation = polygon.triangulated(lambda vertices: np.asarray([[0, 1, 2], [0, 2, 3]], dtype=np.int64))
    assert tessellation.triangles == [[0, 1, 2], [0, 2, 3]]


@pytest.mark.parametrize("kind", ["polygon", "surface", "polyhedron", "mesh"])
@pytest.mark.parametrize(
    ("failure", "message"),
    [
        ("incomplete", "exactly n - 2"),
        ("duplicate", "boundary edge"),
        ("reversed", "boundary edge"),
        ("invalid-incidence", "interior edge"),
        ("degenerate", "degenerate"),
    ],
)
def test_aggregate_triangulation_requires_complete_source_wound_results(kind, failure, message):
    vertices = DEGENERATE_PENTAGON if failure == "degenerate" else PENTAGON
    geometry = make_single_face_geometry(kind, vertices)

    def triangulator(points):
        return invalid_triangulation(failure, len(points))

    with pytest.raises(ValueError, match=message):
        geometry.triangulated(triangulator)


@pytest.mark.parametrize("kind", ["polygon", "surface", "mesh"])
@pytest.mark.parametrize(
    ("vertices", "triangulator"),
    [
        (
            [[0, 0, 0], [2, 0, 0], [2, 2, 0], [1, 1, 0], [0, 2, 0]],
            triangulate_polygon_earclip,
        ),
        (
            [[0, 0, 0], [2, 0, 1], [3, 1, -1], [2, 3, 2], [0, 2, -1]],
            triangulate_polygon_minimum_area,
        ),
    ],
    ids=["concave-planar", "twisted-minimum-area"],
)
def test_aggregate_triangulation_accepts_valid_source_wound_results(kind, vertices, triangulator):
    geometry = make_single_face_geometry(kind, vertices)
    assert len(triangulation_faces(geometry.triangulated(triangulator))) == len(vertices) - 2


def test_polyhedron_triangulation_accepts_valid_concave_source_wound_results():
    vertices = [[0, 0, 0], [2, 0, 0], [2, 2, 0], [1, 1, 0], [0, 2, 0]]
    polyhedron = make_single_face_geometry("polyhedron", vertices)
    assert len(polyhedron.triangulated(triangulate_polygon_earclip).triangles) == 2 * len(vertices) - 2


@pytest.mark.parametrize(
    "geometry",
    [
        Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]),
        PolygonalSurface([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]]),
        Polyhedron.from_platonicsolid(6),
        Mesh.from_polyhedron(6),
    ],
)
def test_nonmutating_aggregate_none_matches_omitted_default(geometry):
    assert triangulation_faces(geometry.triangulated(None)) == triangulation_faces(geometry.triangulated())


def test_mutating_mesh_none_matches_omitted_default():
    omitted = Mesh.from_polyhedron(6)
    explicit_none = omitted.copy()
    omitted.triangulate()
    explicit_none.triangulate(None)
    assert omitted.to_vertices_and_faces() == explicit_none.to_vertices_and_faces()


def test_mesh_triangulate_is_atomic_and_preserves_face_attributes():
    mesh = Mesh.from_vertices_and_faces(
        [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [2, 0, 0], [2, 1, 0]],
        [[0, 1, 2, 3], [1, 4, 5, 2]],
    )
    mesh.face_attribute(0, "source", "first")

    def fail_on_second(vertices):
        if vertices[0][0] == 1:
            raise ValueError("failed")
        return triangulate_polygon(vertices)

    before = mesh.__data__
    with pytest.raises(ValueError, match="failed"):
        mesh.triangulate(fail_on_second)
    assert mesh.__data__ == before

    mesh.triangulate()
    assert mesh.number_of_faces() == 4
    assert sum(mesh.face_attribute(face, "source") == "first" for face in mesh.faces()) == 2


def test_mesh_triangulate_validates_all_callable_results_before_mutating():
    mesh = Mesh.from_vertices_and_faces(
        [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [2, 0, 0], [2, 1, 0]],
        [[0, 1, 2, 3], [1, 4, 5, 2]],
    )
    before = mesh.__data__
    calls = 0

    def invalid_on_second_face(vertices):
        nonlocal calls
        calls += 1
        if calls == 2:
            return [[0, 1, len(vertices)]]
        return triangulate_polygon(vertices)

    with pytest.raises(ValueError, match="refer to vertices"):
        mesh.triangulate(invalid_on_second_face)
    assert mesh.__data__ == before


@pytest.mark.parametrize(
    "failure",
    ["incomplete", "duplicate", "reversed", "invalid-incidence", "degenerate"],
)
def test_mesh_triangulate_rejects_invalid_results_atomically(failure):
    vertices = DEGENERATE_PENTAGON if failure == "degenerate" else PENTAGON
    mesh = Mesh.from_vertices_and_faces(vertices, [list(range(len(vertices)))])
    before = mesh.__data__

    def triangulator(points):
        return invalid_triangulation(failure, len(points))

    with pytest.raises(ValueError):
        mesh.triangulate(triangulator)
    assert mesh.__data__ == before
