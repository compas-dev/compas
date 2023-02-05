from compas.geometry import Circle
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import is_point_in_circle_xy


def test_is_point_in_circle_xy():
    pt = [1, 2, 0]  # only testing in xy
    circle = [[[2, 2, 10], [0, 0, 1]], 4.7]

    assert is_point_in_circle_xy(pt, circle) == True

    pt_outside = [15, 15, 0]
    assert is_point_in_circle_xy(pt_outside, circle) == False


def test_is_point_in_circle_xy_class_input():
    pt_inside = Point(1, 2, 0)
    plane = Plane(Point(2, 2, 10), Vector(0, 0, 1))
    radius = 4.7
    circle = Circle(plane, radius)
    assert is_point_in_circle_xy(pt_inside, circle) == True

    pt_outside = Point(15, 15, 0)
    assert is_point_in_circle_xy(pt_outside, circle) == False
