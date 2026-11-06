import math
from decimal import Decimal

import numpy as np
import pytest

from compas.typing import CoordinateProtocol
from compas.typing import PointsProtocol
from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Pointcloud
from compas.geometry import Polygon
from compas.geometry import PolygonalSurface
from compas.geometry import Polyhedron
from compas.geometry import Polyline
from compas.geometry import Quaternion
from compas.geometry import Transformation
from compas.geometry import intersection_plane_circle
from compas.geometry import is_ccw_xy
from compas.geometry import transform_points
from compas.geometry import Vector
from compas.linalg import length_vector
from compas.tolerance import TOL


class DuckCoordinate:
    def __init__(self, x, y, z):
        self.values = (x, y, z)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __iter__(self):
        return iter(self.values)


class IndexCoordinate:
    def __init__(self, x, y, z):
        self.values = (x, y, z)

    def __getitem__(self, key):
        return self.values[key]


class IterableOnlyCoordinate:
    def __init__(self, *values):
        self.values = values

    def __iter__(self):
        return iter(self.values)


def test_runtime_coordinate_protocol_behavior_is_preserved():
    coordinate = DuckCoordinate(np.float32(1), np.float64(2), 3)

    assert isinstance(coordinate, CoordinateProtocol)
    assert isinstance([coordinate], PointsProtocol)
    assert Point(1, 2, 3) == coordinate


def test_indexing_only_coordinate_remains_usable_by_duck_typing():
    coordinate = IndexCoordinate(1, 2, 2)

    assert not isinstance(coordinate, CoordinateProtocol)
    assert math.isclose(length_vector(coordinate), 3.0)


def test_quaternion_conforms_to_coordinate_protocol_and_supports_slicing():
    quaternion = Quaternion(np.float32(1), np.int64(2), 3, 4)

    assert isinstance(quaternion, CoordinateProtocol)
    assert quaternion[:2] == [1.0, 2.0]
    assert quaternion == np.asarray([1, 2, 3, 4], dtype=np.float32)
    assert quaternion != IterableOnlyCoordinate(1, 2, 3, 4)


def test_builtin_bool_remains_usable_where_an_operation_allows_it():
    assert math.isclose(length_vector((True, False, False)), 1.0)


def test_numpy_comparison_results_are_not_normalized_for_typing():
    scalar = np.float32(1.0)

    assert isinstance(TOL.compare(scalar, scalar, TOL.relative, TOL.absolute), np.bool_)
    assert isinstance(TOL.is_zero(np.float32(0.0)), np.bool_)
    assert isinstance(TOL.is_positive(scalar), np.bool_)
    assert isinstance(TOL.is_negative(-scalar), np.bool_)
    assert isinstance(TOL.is_between(scalar, np.float32(0.0), np.float32(2.0)), np.bool_)
    assert isinstance(
        is_ccw_xy(
            np.asarray([0, 0, 0], dtype=np.float32),
            np.asarray([1, 0, 0], dtype=np.float32),
            np.asarray([0, 1, 0], dtype=np.float32),
        ),
        np.bool_,
    )


def test_datastructure_coordinate_annotations_do_not_add_conversion():
    vertices = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)
    mesh = Mesh.from_vertices_and_faces(vertices, [[0, 1, 2]])

    assert mesh.number_of_vertices() == 3
    assert mesh.vertex_coordinates(1) == [1.0, 0.0, 0.0]


def test_copying_geometry_constructors_accept_numpy_coordinates():
    point = np.asarray([1, 2, 3], dtype=np.float32)
    direction = np.asarray([0, 0, 1], dtype=np.int64)

    plane = Plane(point, direction)
    line = Line(point, np.asarray([4, 5, 6], dtype=np.float64))
    frame = Frame(point, np.asarray([1, 0, 0], dtype=np.float32), np.asarray([0, 1, 0], dtype=np.int32))

    assert plane.point == Point(1, 2, 3)
    assert plane.normal == Vector(0, 0, 1)
    assert line.start == Point(1, 2, 3)
    assert line.end == Point(4, 5, 6)
    assert frame.point == Point(1, 2, 3)


def test_numpy_line_plane_and_matrix_composites_follow_runtime_contracts():
    line = np.asarray([[0, 0, 0], [1, 0, 0]], dtype=np.float32)
    plane = np.asarray([[0, 0, 0], [0, 0, 1]], dtype=np.int64)
    matrix = np.eye(4, dtype=np.float64)

    point = Point(0, 1, 1)
    assert math.isclose(point.distance_to_line(line), math.sqrt(2.0))
    assert math.isclose(point.distance_to_plane(plane), 1.0)
    assert transform_points(np.asarray([[1, 2, 3]], dtype=np.float32), matrix) == [[1.0, 2.0, 3.0]]
    point.transform(matrix)
    assert point == [0, 1, 1]


def test_numpy_scalars_are_accepted_by_circle_and_euler_angle_contracts():
    result = intersection_plane_circle(
        np.asarray([[0, 0, 0], [0, 0, 1]], dtype=np.float32),
        (np.asarray([[0, 0, 0], [1, 0, 0]], dtype=np.float64), np.float32(1.0)),
    )
    transformation = Transformation.from_euler_angles(np.asarray([0, 0, 0], dtype=np.float32))
    decimal_transformation = Transformation.from_euler_angles([Decimal("0"), Decimal("0"), Decimal("0")])

    assert len(result) == 2
    assert transformation == Transformation()
    assert decimal_transformation == Transformation()


def _coordinate_layouts():
    contiguous = np.asarray([1, 2, 3], dtype=np.float32)
    fortran = np.asfortranarray(np.asarray([[1, 2, 3]], dtype=np.float64))[0]
    sliced = np.asarray([1, 0, 2, 0, 3, 0], dtype=np.int64)[::2]
    readonly = contiguous.copy()
    readonly.flags.writeable = False
    return [contiguous, fortran, sliced, readonly]


@pytest.mark.parametrize("coordinates", _coordinate_layouts(), ids=["contiguous", "fortran", "sliced", "readonly"])
def test_point_and_vector_accept_numpy_scalar_layouts_in_constructors_and_setters(coordinates):
    point = Point(*coordinates)
    vector = Vector(*coordinates)

    point.x, point.y, point.z = coordinates
    vector.x, vector.y, vector.z = coordinates

    assert point == [1, 2, 3]
    assert vector == [1, 2, 3]
    assert point[:2] == [1.0, 2.0]
    assert vector[:2] == [1.0, 2.0]


def _point_buffer_layouts():
    contiguous = np.asarray([[0, 0, 0], [1, 0, 0], [1, 1, 0]], dtype=np.float32)
    fortran = np.asfortranarray(contiguous.astype(np.float64))
    expanded = np.zeros((3, 6), dtype=np.int64)
    expanded[:, ::2] = contiguous
    sliced = expanded[:, ::2]
    readonly = contiguous.copy()
    readonly.flags.writeable = False
    return [contiguous, fortran, sliced, readonly]


@pytest.mark.parametrize("coordinates", _point_buffer_layouts(), ids=["contiguous", "fortran", "sliced", "readonly"])
def test_point_collection_constructors_copy_numpy_buffer_layouts(coordinates):
    polyline = Polyline(coordinates)
    polygon = Polygon(coordinates)
    pointcloud = Pointcloud(coordinates)

    polyline.points = coordinates
    polygon.points = coordinates
    pointcloud.points = coordinates

    expected = coordinates.tolist()
    assert [list(point) for point in polyline] == expected
    assert [list(point) for point in polygon] == expected
    assert [list(point) for point in pointcloud] == expected


def test_empty_numpy_point_collections_preserve_existing_outcomes():
    points = np.empty((0, 3), dtype=np.float32)
    faces = np.empty((0, 3), dtype=np.int64)

    assert len(Polyline(points)) == 0
    assert len(Pointcloud(points)) == 0
    with pytest.raises(IndexError):
        Polygon(points)

    surface = PolygonalSurface(points, faces)
    assert surface.vertices == []
    assert surface.faces == []


@pytest.mark.parametrize(
    ("geometry", "equivalent"),
    [
        (Point(1, 2, 3), np.asarray([1, 2, 3], dtype=np.float32)),
        (Vector(1, 2, 3), np.asarray([1, 2, 3], dtype=np.int64)),
        (Plane([0, 0, 0], [0, 0, 1]), np.asarray([[0, 0, 0], [0, 0, 1]], dtype=np.float64)),
        (Line([0, 0, 0], [1, 0, 0]), np.asarray([[0, 0, 0], [1, 0, 0]], dtype=np.float32)),
        (Frame.worldXY(), np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.int64)),
        (Polyline([[0, 0, 0], [1, 0, 0]]), np.asarray([[0, 0, 0], [1, 0, 0]], dtype=np.float64)),
    ],
)
def test_structural_geometry_equality_accepts_numpy_buffers_and_rejects_iterable_only_inputs(geometry, equivalent):
    equivalent.flags.writeable = False

    assert geometry == equivalent
    assert geometry != IterableOnlyCoordinate(*equivalent)


def test_polygonal_geometry_copies_numpy_indices_as_python_ints():
    vertices = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
    faces = np.asarray([[0, 2, 1], [0, 1, 3], [1, 2, 3], [2, 0, 3]], dtype=np.int64)

    surface = PolygonalSurface(vertices, faces)
    polyhedron = Polyhedron(vertices, faces)

    assert surface.faces == faces.tolist()
    assert polyhedron.faces == faces.tolist()
    assert all(type(index) is int for index in surface.faces[0])
    assert all(type(index) is int for index in polyhedron.faces[0])
    assert faces.tolist() == [[0, 2, 1], [0, 1, 3], [1, 2, 3], [2, 0, 3]]


def test_polygonal_surface_numpy_setters_copy_without_mutating_sources():
    vertices = np.asarray([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)
    faces = np.asarray([[0, 1, 2]], dtype=np.int64)
    expected_vertices = vertices.copy()
    expected_faces = faces.copy()
    surface = PolygonalSurface(np.empty((0, 3), dtype=np.float32), np.empty((0, 3), dtype=np.int64))

    surface.vertices = vertices
    surface.faces = faces

    np.testing.assert_array_equal(vertices, expected_vertices)
    np.testing.assert_array_equal(faces, expected_faces)
    assert surface.vertices == expected_vertices.tolist()
    assert surface.faces == expected_faces.tolist()

    vertices[0, 0] = 10
    faces[0, 0] = 2
    assert surface.vertices[0] == [0.0, 0.0, 0.0]
    assert surface.faces[0] == [0, 1, 2]


def test_polygonal_geometry_rejects_boolean_indices_during_copy():
    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]

    for boolean in (True, np.bool_(True)):
        with np.testing.assert_raises(TypeError):
            PolygonalSurface(vertices, [[0, 1, boolean]])
        with np.testing.assert_raises(TypeError):
            Polyhedron(vertices, [[0, 1, boolean]])
