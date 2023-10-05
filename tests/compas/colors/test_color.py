import pytest
import json
import compas
from random import random

from compas.colors import Color
from compas.geometry import allclose


@pytest.mark.parametrize(
    "color",
    [
        (0, 0, 0),
        (1, 1, 1),
        (0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5, 1.0),
        (0.5, 0.5, 0.5, 0.0),
        (random(), random(), random()),
    ],
)
def test_color(color):
    c = Color(*color)
    assert c.r == color[0]
    assert c.g == color[1]
    assert c.b == color[2]
    assert c.a == color[3] if len(color) == 4 else 1.0

    assert allclose(eval(repr(c)), c, tol=1e-12)


def test_color_data():
    color = Color(random(), random(), random(), random())
    other = Color.from_data(json.loads(json.dumps(color.data)))

    assert color.r == other.r
    assert color.g == other.g
    assert color.b == other.b
    assert color.a == other.a

    assert color == other

    if not compas.IPY:
        assert Color.validate_data(color.data)
        assert Color.validate_data(other.data)


def test_color_predefined():
    assert Color.red() == Color(1.0, 0.0, 0.0)
    assert Color.green() == Color(0.0, 1.0, 0.0)
    assert Color.blue() == Color(0.0, 0.0, 1.0)
    assert Color.cyan() == Color(0.0, 1.0, 1.0)
    assert Color.magenta() == Color(1.0, 0.0, 1.0)
    assert Color.yellow() == Color(1.0, 1.0, 0.0)
    assert Color.white() == Color(1.0, 1.0, 1.0)
    assert Color.black() == Color(0.0, 0.0, 0.0)
    assert Color.grey() == Color(0.5, 0.5, 0.5)
    assert Color.orange() == Color(1.0, 0.5, 0.0)
    assert Color.lime() == Color(0.5, 1.0, 0.0)
    assert Color.mint() == Color(0.0, 1.0, 0.5)
    assert Color.azure() == Color(0.0, 0.5, 1.0)
    assert Color.violet() == Color(0.5, 0.0, 1.0)
    assert Color.pink() == Color(1.0, 0.0, 0.5)
    assert Color.brown() == Color(0.5, 0.25, 0.0)
    assert Color.purple() == Color(0.5, 0.0, 0.5)
    assert Color.teal() == Color(0.0, 0.5, 0.5)
    assert Color.olive() == Color(0.5, 0.5, 0.0)
    assert Color.navy() == Color(0.0, 0.0, 0.5)
    assert Color.maroon() == Color(0.5, 0.0, 0.0)
    assert Color.silver() == Color(0.75, 0.75, 0.75)
