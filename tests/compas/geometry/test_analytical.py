from compas.geometry import circle_evaluate
from compas.geometry import ellipse_evaluate
from math import pi


def test_circle():
    threshold = 1e-6
    x, y, z = circle_evaluate(0, 1, 0)
    assert x == 1 and y == 0 and z == 0
    x, y, z = circle_evaluate(0, 1, 1)
    assert x == 1 and y == 0 and z == 1
    x, y, z = circle_evaluate(pi / 2, 1, 0)
    assert x < threshold and x > -threshold and y == 1 and z == 0
    x, y, z = circle_evaluate(0, 0, 0)
    assert x == 0 and y == 0 and z == 0
    x, y, z = circle_evaluate(0, -1, 0)
    assert x == -1 and y == 0 and z == 0


def test_ellipse():
    threshold = 1e-6
    x, y, z = ellipse_evaluate(0, 1, 1, 0)
    assert x == 1 and y == 0 and z == 0
    x, y, z = ellipse_evaluate(0, 2, 1, 1)
    assert x == 2 and y == 0 and z == 1
    x, y, z = ellipse_evaluate(pi / 2, 1, 1, 0)
    assert x < threshold and x > -threshold and y == 1 and z == 0
    x, y, z = ellipse_evaluate(pi / 2, 1, 2, 0)
    assert x < threshold and x > -threshold and y == 2 and z == 0
    x, y, z = ellipse_evaluate(0, 0, 0, 0)
    assert x == 0 and y == 0 and z == 0
    x, y, z = ellipse_evaluate(0, -1, 1, 0)
    assert x == -1 and y == 0 and z == 0
