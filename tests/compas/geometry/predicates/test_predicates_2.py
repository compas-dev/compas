from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Vector
from compas.geometry import is_point_in_circle_xy, is_polygon_in_polygon_xy


def test_is_point_in_circle_xy():
    pt = [1, 2, 0]  # only testing in xy
    circle = [[[2, 2, 10], [0, 0, 1]], 4.7]

    assert is_point_in_circle_xy(pt, circle) is True

    pt_outside = [15, 15, 0]
    assert is_point_in_circle_xy(pt_outside, circle) is False


def test_is_point_in_circle_xy_class_input():
    pt_inside = Point(1, 2, 0)
    plane = Plane(Point(2, 2, 10), Vector(0, 0, 1))
    radius = 4.7
    circle = Circle(plane, radius)
    assert is_point_in_circle_xy(pt_inside, circle) is True

    pt_outside = Point(15, 15, 0)
    assert is_point_in_circle_xy(pt_outside, circle) is False


def test_is_polygon_in_polygon_xy():
    polygon_contour = Polygon([(0, 0, 0), (4, 2, 0), (10, 0, 0), (11, 10, 0), (8, 12, 0), (0, 10, 0)])
    polygon_inside = Polygon([(5, 5, 0), (10, 5, 0), (10, 10, 0), (5, 10, 0)])
    assert is_polygon_in_polygon_xy(polygon_contour, polygon_inside)

    polygon_outside = Polygon([(15, 5, 0), (20, 5, 0), (20, 10, 0), (15, 10, 0)])
    assert not is_polygon_in_polygon_xy(polygon_contour, polygon_outside)

    polygon_intersecting = Polygon([(10, 10, 0), (10, 5, 0), (15, 5, 0), (15, 10, 0)])
    assert not is_polygon_in_polygon_xy(polygon_contour, polygon_intersecting)

    # shifting the vertices list of the same polygon shouldn't affect the containment check output anymore
    polygon_intersecting_shifted = Polygon(polygon_intersecting[1:] + polygon_intersecting[:1])
    assert not is_polygon_in_polygon_xy(polygon_contour, polygon_intersecting_shifted)
