from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Vector
from compas.geometry import is_point_in_circle_xy, is_polygon_in_polygon_xy
from compas.geometry.predicates.predicates_2 import polygon_to_polygon_relationship_xy, point_to_polygon_relationship_xy, is_intersection_polygon_polygon_xy


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
    polygon_inside = Polygon([(5, 5, 0), (10, 5, 0), (10, 10 ,0), (5, 10, 0)])
    assert is_polygon_in_polygon_xy(polygon_contour, polygon_inside) is True

    polygon_outside = Polygon([(15, 5, 0), (20, 5, 0), (20, 10, 0), (15, 10, 0)])
    assert is_polygon_in_polygon_xy(polygon_contour, polygon_outside) is False

    polygon_intersecting = Polygon([(10, 10, 0), (10, 5, 0), (15, 5, 0), (15, 10, 0)])
    assert is_polygon_in_polygon_xy(polygon_contour, polygon_intersecting) is False

    # shifting the vertices list of the same polygon shouldn't affect the containment check output anymore
    polygon_intersecting_shifted = Polygon(polygon_intersecting[1:] + polygon_intersecting[:1])
    assert is_polygon_in_polygon_xy(polygon_contour, polygon_intersecting_shifted) is False


def test_polygon_to_polygon_relationship_xy():
    polygon_contour = Polygon([(0, 0, 0), (4, 2, 0), (10, 0, 0), (11, 10, 0), (8, 12, 0), (0, 10, 0)])
    polygon_inside = Polygon([(5, 5, 0), (10, 5, 0), (10, 10 ,0), (5, 10, 0)])
    polygon_intersecting = Polygon([(10, 10, 0), (10, 5, 0), (15, 5, 0), (15, 10, 0)])
    polygon_outside = Polygon([(15, 5, 0), (20, 5, 0), (20, 10, 0), (15, 10, 0)])
    polygon_containing = Polygon([(-5, -5, 0), (15, -5, 0), (15, 15, 0), (-5, 15, 0)])

    assert polygon_to_polygon_relationship_xy(polygon_inside, polygon_contour) == 1
    assert polygon_to_polygon_relationship_xy(polygon_intersecting, polygon_contour) == 0
    assert polygon_to_polygon_relationship_xy(polygon_outside, polygon_contour) == -1
    assert polygon_to_polygon_relationship_xy(polygon_containing, polygon_contour) == -2


def test_point_to_polygon_relationship_xy():
    polygon = Polygon([(0, 0, 0), (4, 0, 0), (4, 4, 0), (0, 4, 0)])
    pt_inside = Point(1, 2, 0)
    pt_boundary = Point(2, 0, 0)
    pt_outside = Point(5, 5, 0)

    assert point_to_polygon_relationship_xy(pt_inside, polygon) == 1
    assert point_to_polygon_relationship_xy(pt_boundary, polygon) == 0
    assert point_to_polygon_relationship_xy(pt_outside, polygon) == -1


def test_is_intersection_polygon_polygon_xy():
    polygon_contour = Polygon([(0, 0, 0), (4, 2, 0), (10, 0, 0), (11, 10, 0), (8, 12, 0), (0, 10, 0)])
    polygon_inside = Polygon([(5, 5, 0), (10, 5, 0), (10, 10 ,0), (5, 10, 0)])
    polygon_intersecting = Polygon([(10, 10, 0), (10, 5, 0), (15, 5, 0), (15, 10, 0)])
    polygon_outside = Polygon([(15, 5, 0), (20, 5, 0), (20, 10, 0), (15, 10, 0)])

    assert is_intersection_polygon_polygon_xy(polygon_inside, polygon_contour) is False
    assert is_intersection_polygon_polygon_xy(polygon_intersecting, polygon_contour) is True
    assert is_intersection_polygon_polygon_xy(polygon_outside, polygon_contour) is False