import pytest
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import normalize_vector
from compas.geometry import subtract_vectors
from compas.geometry import distance_point_point
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Frame
from compas.geometry import Line


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
def test_create_line(p1, p2):
    line = Line(p1, p2)

    assert line.start == p1
    assert line.end == p2


# =============================================================================
# Constructors
# =============================================================================


@pytest.mark.parametrize(
    "point, vector",
    [
        ([0, 0, 0], [0, 0, 0]),
        ([0, 0, 0], [1, 0, 0]),
        ([0, 0, 0], [1, 2, 3]),
        (Point(0, 0, 0), Vector(0, 0, 0)),
        (Point(0, 0, 0), Vector(1, 0, 0)),
        (Point(0, 0, 0), Vector(1, 2, 3)),
    ],
)
def test_create_line_from_point_and_vector(point, vector):
    line = Line.from_point_and_vector(point, vector)

    assert line.start == point
    assert line.end == add_vectors(point, vector)


@pytest.mark.parametrize(
    "point, direction, length",
    [
        # ([0, 0, 0], [0, 0, 0], 3.0),
        ([0, 0, 0], [1, 0, 0], 3.0),
        ([0, 0, 0], [1, 2, 3], 3.0),
        # (Point(0, 0, 0), Vector(0, 0, 0), 3.0),
        (Point(0, 0, 0), Vector(1, 0, 0), 3.0),
        (Point(0, 0, 0), Vector(1, 2, 3), 3.0),
    ],
)
def test_create_line_from_point_direction_length(point, direction, length):
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

    assert line.frame == Frame.worldXY()

    with pytest.raises(AttributeError):
        line.frame = Frame.worldZX()

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
