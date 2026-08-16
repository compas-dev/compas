from copy import deepcopy
import pytest
import json

from compas.linalg import add_vectors
from compas.linalg import scale_vector
from compas.linalg import normalize_vector
from compas.linalg import subtract_vectors
from compas.geometry import distance_point_point
from compas.geometry import Point
from compas.geometry import Translation
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Line
from compas.geometry import Curve
from compas.tolerance import TOL


@pytest.mark.parametrize(
    "p1,p2",
    [
        ([0, 0, 0], [0, 0, 0]),
        ([0, 0, 0], [1, 0, 0]),
        ([0, 0, 0], [1, 2, 3]),
        (Point(0, 0, 0), Point(0, 0, 0)),
        (Point(0, 0, 0), Point(1, 0, 0)),
        (Point(0, 0, 0), Point(1, 2, 3)),
        (Point(0, 0, 0), [0, 0, 0]),
        (Point(0, 0, 0), [1, 0, 0]),
        (Point(0, 0, 0), [1, 2, 3]),
        ([0, 0, 0], Point(0, 0, 0)),
        ([0, 0, 0], Point(1, 0, 0)),
        ([0, 0, 0], Point(1, 2, 3)),
    ],
)
def test_line_create(p1, p2):
    line = Line(p1, p2)

    assert line.start == p1
    assert line.end == p2


def test_line_is_primitive_geometry():
    assert issubclass(Line, Geometry)
    assert not issubclass(Line, Curve)
    assert Line.__module__ == "compas.geometry.line"


def test_line_create_with_frame():
    with pytest.raises(TypeError):
        Line([0, 0, 0], [1, 0, 0], frame=Frame.worldXY())


def test_line_rejects_2d_coordinates():
    with pytest.raises(IndexError):
        Line([0, 0], [1, 0, 0])

    with pytest.raises(IndexError):
        Line([0, 0, 0], [1, 0])


# =============================================================================
# Data
# =============================================================================


def test_line_data():
    line = Line([0, 0, 0], [1, 0, 0])
    other = Line.__from_data__(json.loads(json.dumps(line.__data__)))

    assert line.start == other.start
    assert line.end == other.end


# =============================================================================
# Constructors
# =============================================================================


@pytest.mark.parametrize(
    "point,vector",
    [
        ([0, 0, 0], [0, 0, 0]),
        ([0, 0, 0], [1, 0, 0]),
        ([0, 0, 0], [1, 2, 3]),
        (Point(0, 0, 0), Vector(0, 0, 0)),
        (Point(0, 0, 0), Vector(1, 0, 0)),
        (Point(0, 0, 0), Vector(1, 2, 3)),
    ],
)
def test_line_create_from_point_and_vector(point, vector):
    line = Line.from_point_and_vector(point, vector)

    assert line.start == point
    assert line.end == add_vectors(point, vector)


@pytest.mark.parametrize(
    "point,direction,length",
    [
        # ([0, 0, 0], [0, 0, 0], 3.0),
        ([0, 0, 0], [1, 0, 0], 3.0),
        ([0, 0, 0], [1, 2, 3], 3.0),
        # (Point(0, 0, 0), Vector(0, 0, 0), 3.0),
        (Point(0, 0, 0), Vector(1, 0, 0), 3.0),
        (Point(0, 0, 0), Vector(1, 2, 3), 3.0),
    ],
)
def test_line_create_from_point_direction_length(point, direction, length):
    line = Line.from_point_direction_length(point, direction, length)

    assert line.start == point
    assert line.end == add_vectors(point, scale_vector(normalize_vector(direction), length))


# =============================================================================
# Properties and Geometry
# =============================================================================


@pytest.mark.parametrize(
    "p1,p2",
    [
        # ([0, 0, 0], [0, 0, 0]),
        ([0, 0, 0], [1, 0, 0]),
        ([0, 0, 0], [1, 2, 3]),
        # (Point(0, 0, 0), Point(0, 0, 0)),
        (Point(0, 0, 0), Point(1, 0, 0)),
        (Point(0, 0, 0), Point(1, 2, 3)),
        # (Point(0, 0, 0), [0, 0, 0]),
        (Point(0, 0, 0), [1, 0, 0]),
        (Point(0, 0, 0), [1, 2, 3]),
        # ([0, 0, 0], Point(0, 0, 0)),
        ([0, 0, 0], Point(1, 0, 0)),
        ([0, 0, 0], Point(1, 2, 3)),
    ],
)
def test_line_properties(p1, p2):
    line = Line(p1, p2)

    assert line.start == p1
    assert line.end == p2
    assert line.vector == subtract_vectors(p2, p1)
    assert line.direction == normalize_vector(subtract_vectors(p2, p1))
    assert line.length == distance_point_point(p1, p2)

    line._point = None
    with pytest.raises(ValueError):
        line.point

    line._vector = None
    with pytest.raises(ValueError):
        line.vector


@pytest.mark.parametrize(
    "p1,p2",
    [
        # ([0, 0, 0], [0, 0, 0]),
        ([0, 0, 0], [1, 0, 0]),
        ([0, 0, 0], [1, 2, 3]),
        # (Point(0, 0, 0), Point(0, 0, 0)),
        (Point(0, 0, 0), Point(1, 0, 0)),
        (Point(0, 0, 0), Point(1, 2, 3)),
        # (Point(0, 0, 0), [0, 0, 0]),
        (Point(0, 0, 0), [1, 0, 0]),
        (Point(0, 0, 0), [1, 2, 3]),
        # ([0, 0, 0], Point(0, 0, 0)),
        ([0, 0, 0], Point(1, 0, 0)),
        ([0, 0, 0], Point(1, 2, 3)),
    ],
)
def test_line_geometry(p1, p2):
    line = Line(p1, p2)

    assert line.point_at(0.0) == p1
    assert line.point_at(1.0) == p2
    assert line.point_at(0.5) == scale_vector(add_vectors(p1, p2), 0.5)


# =============================================================================
# Accessors
# =============================================================================


@pytest.mark.parametrize(
    "p1,p2",
    [
        # ([0, 0, 0], [0, 0, 0]),
        ([0, 0, 0], [1, 0, 0]),
        ([0, 0, 0], [1, 2, 3]),
        # (Point(0, 0, 0), Point(0, 0, 0)),
        (Point(0, 0, 0), Point(1, 0, 0)),
        (Point(0, 0, 0), Point(1, 2, 3)),
        # (Point(0, 0, 0), [0, 0, 0]),
        (Point(0, 0, 0), [1, 0, 0]),
        (Point(0, 0, 0), [1, 2, 3]),
        # ([0, 0, 0], Point(0, 0, 0)),
        ([0, 0, 0], Point(1, 0, 0)),
        ([0, 0, 0], Point(1, 2, 3)),
    ],
)
def test_line_accessors(p1, p2):
    line = Line(p1, p2)

    assert line[0] == p1
    assert line[1] == p2
    assert len(line) == 2

    for index, point in enumerate(line):
        if index == 0:
            assert point == p1
        elif index == 1:
            assert point == p2
        else:
            assert False


# =============================================================================
# Comparison
# =============================================================================

# =============================================================================
# Other Methods
# =============================================================================


@pytest.mark.parametrize(
    "p1,p2",
    [
        ([0, 0, 0], [1, 0, 0]),
        ([0, 0, 0], [1, 2, 3]),
        ([1, 2, 3], [-1, -2, -3]),
        ([-11.1, 22.2, 33.3], [1.1, -2.2, -3.3]),
    ],
)
def test_line_point_from_start(p1, p2):
    distances = [0, 1, 4, -9, 3.3, 0.00001, -0.00001]
    for distance in distances:
        line = Line(p1, p2)
        point = line.point_from_start(distance)
        distance_to_start = distance_point_point(point, p1)
        distance_to_end = distance_point_point(point, p2)
        # Check that the distance is correct
        assert TOL.is_close(distance_to_start, abs(distance))
        # Check that negative distance gives a point far away from end
        if distance < 0:
            assert distance_to_end > line.length


@pytest.mark.parametrize(
    "p1,p2",
    [
        ([0, 0, 0], [1, 0, 0]),
        ([0, 0, 0], [1, 2, 3]),
        ([1, 2, 3], [-1, -2, -3]),
        ([-11.1, 22.2, 33.3], [1.1, -2.2, -3.3]),
    ],
)
def test_line_point_from_end(p1, p2):
    distances = [0, 1, 4, -9, 3.3, 0.00001, -0.00001]
    for distance in distances:
        line = Line(p1, p2)
        point = line.point_from_end(distance)
        assert isinstance(point, Point)
        distance_to_start = distance_point_point(point, p1)
        distance_to_end = distance_point_point(point, p2)
        # Check that the distance is correct
        assert TOL.is_close(distance_to_end, abs(distance))
        # Check that negative distance gives a point far away from start
        if distance < 0:
            assert distance_to_start > line.length


@pytest.mark.parametrize(
    "p1,p2",
    [
        ([0, 0, 0], [1, 0, 0]),
        ([0, 0, 0], [1, 2, 3]),
        ([1, 2, 3], [-1, -2, -3]),
        ([-11.1, 22.2, 33.3], [1.1, -2.2, -3.3]),
    ],
)
def test_line_flip(p1, p2):
    line = Line(p1, p2)
    line.flip()
    assert TOL.is_zero(distance_point_point(line.start, p2))
    assert TOL.is_zero(distance_point_point(line.end, p1))
    flipped_line = Line(p1, p2).flipped()
    assert TOL.is_zero(distance_point_point(flipped_line.start, p2))
    assert TOL.is_zero(distance_point_point(flipped_line.end, p1))


def test_line_copy_deepcopy():
    line = Line([0, 0, 0], [1, 0, 0])

    line_copy = line.copy()

    assert line is not line_copy
    assert line == line_copy

    line_deepcopy = deepcopy(line)

    assert line is not line_deepcopy
    assert line == line_deepcopy


def test_line_sequence_mutation_and_comparison():
    line = Line([0, 0, 0], [1, 0, 0])

    line[0] = [1, 2, 3]
    line[1] = [4, 5, 6]

    assert list(line) == [line.start, line.end]
    assert line == [[1, 2, 3], [4, 5, 6]]
    assert line != [[1, 2, 3]]
    assert line != object()

    with pytest.raises(KeyError):
        _ = line[2]

    with pytest.raises(KeyError):
        line[2] = [0, 0, 0]


def test_line_midpoint_and_closest_point():
    line = Line([0, 0, 0], [2, 0, 0])
    point = Point(1, 2, 0)

    assert line.midpoint == [1, 0, 0]
    assert line.closest_point(point) == [1, 0, 0]
    assert line.closest_point([1, 2, 0]) == [1, 0, 0]

    with pytest.raises(IndexError):
        line.closest_point([1, 2])

    closest, parameter = line.closest_point(point, return_parameter=True)
    assert closest == [1, 0, 0]
    assert parameter == 0.5


def test_line_transform():
    line = Line([0, 0, 0], [1, 0, 0])
    line.transform(Translation.from_vector([1, 2, 3]))

    assert line.start == [1, 2, 3]
    assert line.end == [2, 2, 3]


def test_line_flipped_preserves_subclass():
    class CustomLine(Line):
        pass

    line = CustomLine([0, 0, 0], [1, 2, 3])
    flipped = line.flipped()

    assert isinstance(flipped, CustomLine)
    assert flipped.start == line.end
    assert flipped.end == line.start


@pytest.mark.parametrize(
    "operation",
    [
        lambda line: line.direction,
        lambda line: line.point_from_start(1),
        lambda line: line.point_from_end(1),
        lambda line: line.closest_point(Point(1, 0, 0)),
    ],
)
def test_zero_length_line_raises_zero_division_error(operation):
    line = Line([0, 0, 0], [0, 0, 0])

    with pytest.raises(ZeroDivisionError):
        operation(line)
