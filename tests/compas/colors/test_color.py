import pytest
import json
from random import random

from compas.colors import Color
from compas.colors import ColorError
from compas.tolerance import TOL


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

    assert TOL.is_allclose(eval(repr(c)), c)


@pytest.mark.parametrize("component", [float("nan"), float("inf"), float("-inf")])
def test_color_rejects_nonfinite_components(component):
    with pytest.raises(ValueError, match="range 0-1"):
        Color(component, 0.0, 0.0)

    color = Color.black()
    with pytest.raises(ValueError, match="range 0-1"):
        color.a = component


def test_color_rejects_boolean_components():
    with pytest.raises(ValueError, match="range 0-1"):
        Color(True, 0.0, 0.0)

    color = Color.black()
    with pytest.raises(ValueError, match="range 0-1"):
        color.a = False


def test_color_data():
    color = Color(random(), random(), random(), random())
    other = Color.__from_data__(json.loads(json.dumps(color.__data__)))

    assert color.r == other.r
    assert color.g == other.g
    assert color.b == other.b
    assert color.a == other.a

    assert color == other


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


def test_color_comparison_with_unrelated_and_short_values():
    color = Color.red()

    assert color != object()
    assert color != [1.0]
    assert color == [1.0, 0.0, 0.0]
    assert color == [1.0, 0.0, 0.0, 1.0]
    assert color != [1.0, 0.0, 0.0, 0.5]
    assert color != Color(1.0, 0.0, 0.0, 0.5)
    assert Color(1.0, 0.0, 0.0, 0.5) == [1.0, 0.0, 0.0, 0.5]
    assert Color(1.0, 0.0, 0.0, 0.5) != [1.0, 0.0, 0.0]


def test_color_hex_supports_short_and_long_forms():
    assert Color.from_hex("#f00") == Color.red()
    assert Color.from_hex("f00") == Color.red()
    assert Color.from_hex("#ff0000") == Color.red()
    assert Color.from_hex("ff0000") == Color.red()

    with pytest.raises(ValueError):
        Color.from_hex("#ff00")


@pytest.mark.parametrize("component", [0, 1, 127, 128, 254, 255])
def test_rgb255_roundtrip(component):
    color = Color.from_rgb255(component, component, component)
    assert color.rgb255 == (component, component, component)


def test_rgb255_uses_nearest_integer():
    color = Color(0.5, 0.5, 0.5, 0.5)
    assert color.rgb255 == (128, 128, 128)
    assert color.rgba255 == (128, 128, 128, 128)
    assert color.hex == "#808080"


def test_color_coercion():
    assert Color.coerce(None) is None
    assert Color.coerce("red") == Color.red()
    assert Color.coerce("#f00") == Color.red()
    assert Color.coerce("ff0000") == Color.red()
    assert Color.coerce((255, 0, 0)) == Color.red()
    assert Color.coerce((1.0, 0.0, 0.0)) == Color.red()
    assert Color.coerce((1, 0.5, 0)) == Color(1.0, 0.5, 0.0)

    with pytest.raises(ColorError):
        Color.coerce((1.0, 0.0))
    with pytest.raises(ColorError):
        Color.coerce((True, False, False))
    with pytest.raises(ColorError):
        Color.coerce((255.0, 0.0, 0.0))


def test_black_has_zero_saturation():
    assert Color.black().saturation == 0.0


def test_relative_luminance_uses_linear_srgb():
    assert Color.black().luminance == 0.0
    assert Color.white().luminance == 1.0
    assert Color.red().luminance == pytest.approx(0.2126)
    assert Color(0.5, 0.5, 0.5).luminance == pytest.approx(0.21404114048223255)


def test_is_light_uses_relative_luminance_threshold():
    assert Color.from_hex("#767676").is_light
    assert not Color.from_hex("#757575").is_light


def test_color_constructors_preserve_subclasses():
    class CustomColor(Color):
        pass

    assert isinstance(CustomColor.red(), CustomColor)
    assert isinstance(CustomColor.from_hex("#f00"), CustomColor)
    assert isinstance(CustomColor.coerce("red"), CustomColor)
    color = CustomColor.coerce(Color(1.0, 0.0, 0.0, 0.5))
    assert isinstance(color, CustomColor)
    assert color == Color(1.0, 0.0, 0.0, 0.5)
