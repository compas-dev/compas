import compas
import pytest

from compas.colors import Color
from compas.colors import ColorMap


def test_colormap_requires_256_colors():
    with pytest.raises(ValueError, match="256"):
        ColorMap([Color.red()])


def test_colormap_copies_colors_and_preserves_alpha():
    colors = [Color(1.0, 0.0, 0.0, 0.5) for _ in range(256)]
    colormap = ColorMap(colors)
    colors[0].r = 0.0

    assert colormap.colors[0].rgb == Color.red().rgb
    assert colormap.colors[0].a == 0.5


def test_colormap_colors_are_immutable():
    colormap = ColorMap.from_mpl("viridis")
    assert isinstance(colormap.colors, tuple)

    with pytest.raises(TypeError):
        colormap.colors[0] = Color.red()


def test_colormap_lookup():
    colormap = ColorMap.from_two_colors(Color.black(), Color.white())

    assert colormap(0.0) == Color.black()
    assert colormap(1.0) == Color.white()
    assert colormap(5.0, minval=0.0, maxval=10.0) == colormap.colors[127]

    with pytest.raises(KeyError):
        colormap(11.0, minval=0.0, maxval=10.0)
    with pytest.raises(ValueError, match="nonzero"):
        colormap(1.0, minval=1.0, maxval=1.0)


def test_colormap_data_roundtrip():
    colormap = ColorMap.from_mpl("viridis")
    reconstructed = compas.json_loads(compas.json_dumps(colormap))

    assert isinstance(reconstructed, ColorMap)
    assert reconstructed.colors == colormap.colors


def test_colormap_constructors():
    assert len(ColorMap.from_palette("bamako").colors) == 256
    assert len(ColorMap.from_mpl("viridis").colors) == 256
    assert len(ColorMap.from_color(Color.red(), "light").colors) == 256
    assert len(ColorMap.from_three_colors(Color.red(), Color.white(), Color.blue()).colors) == 256
    assert len(ColorMap.from_rgb().colors) == 256


def test_colormap_constructors_preserve_subclasses():
    class CustomColorMap(ColorMap):
        pass

    assert isinstance(CustomColorMap.from_mpl("viridis"), CustomColorMap)
    assert isinstance(CustomColorMap.from_two_colors(Color.red(), Color.blue()), CustomColorMap)
