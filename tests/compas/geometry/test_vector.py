import pytest
import json
import compas
from random import random
from compas.geometry import Vector
from compas.tolerance import TOL


@pytest.mark.parametrize(
    "x,y,z",
    [
        (1, 2, 3),
        (1.0, 2.0, 3.0),
        ("1.0", "2", 3.0),
        (random(), random(), random()),
    ],
)
def test_vector(x, y, z):
    v = Vector(x, y, z)
    x, y, z = float(x), float(y), float(z)
    assert v.x == x and v.y == y and v.z == z
    assert v[0] == x and v[1] == y and v[2] == z

    if not compas.IPY:
        assert eval(repr(v)) == v


@pytest.mark.parametrize(
    "x,y",
    [
        (1, 2),
        (1.0, 2.0),
        ("1.0", "2"),
        (random(), random()),
    ],
)
def test_vector2(x, y):
    v = Vector(x, y)
    x, y, z = float(x), float(y), 0.0
    assert v.x == x and v.y == y and v.z == z
    assert v[0] == x and v[1] == y and v[2] == z

    if not compas.IPY:
        assert eval(repr(v)) == v


def test_vector_operators():
    a = Vector(random(), random(), random())
    b = Vector(random(), random(), random())
    c = [random(), random(), random()]

    assert a * 2 == [a.x * 2, a.y * 2, a.z * 2]
    assert a / 2 == [a.x / 2, a.y / 2, a.z / 2]
    assert a**3 == [a.x**3, a.y**3, a.z**3]
    assert 2 * a == [2 * a.x, 2 * a.y, 2 * a.z]

    assert a + b == [a.x + b.x, a.y + b.y, a.z + b.z]
    assert a - b == [a.x - b.x, a.y - b.y, a.z - b.z]
    assert a * b == [a.x * b.x, a.y * b.y, a.z * b.z]
    assert a / b == [a.x / b.x, a.y / b.y, a.z / b.z]

    assert b + a == [a.x + b.x, a.y + b.y, a.z + b.z]
    assert b - a == [b.x - a.x, b.y - a.y, b.z - a.z]
    assert b * a == [a.x * b.x, a.y * b.y, a.z * b.z]
    assert b / a == [b.x / a.x, b.y / a.y, b.z / a.z]

    assert a * c == [a.x * c[0], a.y * c[1], a.z * c[2]]
    assert c * a == [a.x * c[0], a.y * c[1], a.z * c[2]]
    assert a + c == [a.x + c[0], a.y + c[1], a.z + c[2]]
    assert a - c == [a.x - c[0], a.y - c[1], a.z - c[2]]

    assert c * a == [a.x * c[0], a.y * c[1], a.z * c[2]]
    assert c / a == [c[0] / a.x, c[1] / a.y, c[2] / a.z]
    assert c + a == [a.x + c[0], a.y + c[1], a.z + c[2]]
    assert c - a == [c[0] - a.x, c[1] - a.y, c[2] - a.z]

    with pytest.raises(TypeError) as exc_info:
        a / "wrong type"
    if not compas.IPY:
        assert str(exc_info.value) == "Cannot cast wrong type <class 'str'> to Vector"

    with pytest.raises(TypeError) as exc_info:
        a * "wrong type"
    if not compas.IPY:
        assert str(exc_info.value) == "Cannot cast wrong type <class 'str'> to Vector"


def test_vector_equality():
    p1 = Vector(1, 1, 1)
    p2 = Vector(1, 1, 1)
    p3 = Vector(0, 0, 0)
    assert p1 == p2
    assert not (p1 != p2)
    assert p1 != p3
    assert not (p1 == p3)
    assert p1 != [1, 1]
    assert p1 != [1, 1, 1, 1]
    assert p1 != object()
    assert p1 is not None


def test_vector_comparison_relative():
    a = Vector(random(), random(), random())
    b = Vector(a.x + a.x * TOL.relative * 0.1, a.y + a.y * TOL.relative * 0.1, a.z + a.z * TOL.relative * 0.1)
    c = Vector(a.x + a.x * TOL.relative, a.y + a.y * TOL.relative, a.z + a.z * TOL.relative)
    d = Vector(a.x + a.x * TOL.relative * 10.0, a.y + a.y * TOL.relative * 10.0, a.z + a.z * TOL.relative * 10.0)
    assert a == b
    assert a == c
    assert a != d


def test_vector_comparison_absolute():
    a = Vector(0, 0, 0)
    b = Vector(a.x + TOL.absolute * 0.1, a.y + TOL.absolute * 0.1, a.z + TOL.absolute * 0.1)
    c = Vector(a.x + TOL.absolute, a.y + TOL.absolute, a.z + TOL.absolute)
    d = Vector(a.x + TOL.absolute * 10.0, a.y + TOL.absolute * 10.0, a.z + TOL.absolute * 10.0)
    assert a == b
    assert a == c
    assert a != d


def test_vector_inplace_operators():
    vector = Vector(2.0, 4.0, 6.0)
    identity = id(vector)

    vector += [1.0, 2.0, 3.0]
    vector -= [1.0, 1.0, 1.0]
    vector *= 2.0
    vector /= 4.0
    vector **= 2.0

    assert id(vector) == identity
    assert vector == [1.0, 6.25, 16.0]


def test_vector_sequence_behaviour():
    vector = Vector(1.0, 2.0, 3.0)

    assert len(vector) == 3
    assert list(vector) == [1.0, 2.0, 3.0]
    assert vector[:] == [1.0, 2.0, 3.0]
    assert vector[-3] == 1.0
    assert vector[-1] == 3.0

    vector[0] = 4.0
    vector[-2] = 5.0
    vector[-1] = 6.0
    assert vector == [4.0, 5.0, 6.0]

    with pytest.raises(IndexError):
        _ = vector[3]
    with pytest.raises(IndexError):
        _ = vector[-4]
    with pytest.raises(IndexError):
        vector[3] = 7.0
    with pytest.raises(IndexError):
        vector[-4] = 7.0


def test_vector_scale():
    vector = Vector(1.0, 2.0, 3.0)
    vector.scale(2.0, 3.0, 4.0)
    assert vector == [2.0, 6.0, 12.0]

    scaled = vector.scaled(0.5)
    assert scaled == [1.0, 3.0, 6.0]
    assert scaled is not vector


def test_vector_data():
    vector = Vector(random(), random(), random())
    other = Vector.__from_data__(json.loads(json.dumps(vector.__data__)))

    assert vector == other
    assert vector.__data__ == other.__data__
    assert vector.guid != other.guid


def test_cross_vectors():
    vec_list1 = [[1, 2, 3], [7, 8, 9]]
    vec_list2 = [[2, 3, 4], [5, 6, 7]]

    result = Vector.cross_vectors(vec_list1, vec_list2)
    assert result == [[-1, 2, -1], [2, -4, 2]]


def test_cross():
    vec1 = Vector(1, 2, 3)
    vec2 = [5, 6, 7]

    result = vec1.cross(vec2)
    assert result == (-4, 8, -4)
    assert result == Vector(-4, 8, -4)
