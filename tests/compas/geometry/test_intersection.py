import pytest

from compas.geometry import Circle
from compas.geometry import Geometry
from compas.geometry import Intersection
from compas.geometry import IntersectionResult
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import intersection


def test_line_line_intersection():
    a = Line([-1.0, 0.0, 0.0], [1.0, 0.0, 0.0])
    b = Line([0.0, -1.0, 0.0], [0.0, 1.0, 0.0])

    result = intersection(a, b)

    assert isinstance(result, IntersectionResult)
    assert result.number_of_intersections == 1
    assert result.points[0] == [0.0, 0.0, 0.0]


@pytest.mark.parametrize(
    "a, b",
    [
        (Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]), Line([0.0, 0.0, 1.0], [0.0, 1.0, 1.0])),
        (Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]), Line([0.0, 1.0, 0.0], [1.0, 1.0, 0.0])),
    ],
)
def test_nonintersecting_lines_return_empty_result(a, b):
    assert not intersection(a, b)


def test_line_plane_dispatch_is_symmetric():
    line = Line([0.0, 0.0, -1.0], [0.0, 0.0, 1.0])
    plane = Plane.worldXY()

    forward = intersection(line, plane)
    reverse = intersection(plane, line)

    assert forward == reverse
    assert forward.points[0] == [0.0, 0.0, 0.0]


def test_plane_plane_intersection():
    result = intersection(Plane.worldXY(), Plane.worldYZ())

    assert len(result.lines) == 1
    assert Plane.worldXY().contains_point(result.lines[0].start)
    assert Plane.worldYZ().contains_point(result.lines[0].start)


def test_parallel_planes_return_empty_result_regardless_of_normal_orientation():
    assert not intersection(Plane.worldXY(), Plane([0.0, 0.0, 1.0], [0.0, 0.0, 1.0]))
    assert not intersection(Plane.worldXY(), Plane([0.0, 0.0, 1.0], [0.0, 0.0, -1.0]))


def test_unsupported_intersection_combination():
    with pytest.raises(TypeError, match="Circle"):
        intersection(Circle(1.0), Plane.worldXY())


def test_custom_intersection_registration_is_symmetric_and_supports_subclasses():
    class A(Geometry):
        pass

    class B(Geometry):
        pass

    class SubA(A):
        pass

    dispatcher = Intersection()

    @dispatcher.register(A, B)
    def intersection_a_b(a, b, tol=None):
        assert isinstance(a, A)
        assert isinstance(b, B)
        return IntersectionResult((Point(1.0, 2.0, 3.0),))

    assert dispatcher(SubA(), B()).points[0] == [1.0, 2.0, 3.0]
    assert dispatcher(B(), SubA()).points[0] == [1.0, 2.0, 3.0]


def test_duplicate_symmetric_registration_is_rejected():
    dispatcher = Intersection()

    @dispatcher.register(Line, Plane)
    def intersection_line_plane(line, plane, tol=None):
        return IntersectionResult()

    with pytest.raises(ValueError, match="already registered"):

        @dispatcher.register(Plane, Line)
        def intersection_plane_line(plane, line, tol=None):
            return IntersectionResult()
