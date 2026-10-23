import compas
import pytest
from collections.abc import MutableMapping

from compas.colors import Color
from compas.colors import ColorDict
from compas.colors import ColorError


def test_colordict():
    cd = ColorDict(Color.red())
    assert isinstance(cd, MutableMapping)
    assert cd.default == Color.red()

    cd = ColorDict((255, 0, 0))
    assert cd.default == Color.red()

    cd = ColorDict((1.0, 0.0, 0.0))
    assert cd.default == Color.red()


def test_colordict_keys():
    cd = ColorDict(Color.red())
    cd[1] = Color.blue()
    cd[(1, 0)] = Color.green()

    assert cd[1] == Color.blue()
    assert cd["1"] == Color.red()

    assert cd[(1, 0)] == Color.green()
    assert cd[(0, 1)] == Color.red()


def test_colordict_json():
    cd1 = ColorDict(Color.red())
    cd1[1] = Color.blue()
    cd1[(1, 0)] = Color.green()

    cd2 = compas.json_loads(compas.json_dumps(cd1))

    assert cd2[1] == Color.blue()
    assert cd2["1"] == Color.red()

    assert cd2[(1, 0)] == Color.green()
    assert cd2[(0, 1)] == Color.red()


def test_colordict_default_and_mapping_methods():
    colors = ColorDict()
    colors.update({1: "red", (2, 1): (0, 0, 255)})

    assert colors.default == Color.black()
    assert colors[1] == Color.red()
    assert colors[(2, 1)] == Color.blue()
    assert colors[(1, 2)] == Color.black()
    assert list(colors.keys()) == [1, (2, 1)]
    assert list(colors.values()) == [Color.red(), Color.blue()]
    assert colors.get("missing", "lime") == Color.black()
    assert colors["missing"] == Color.black()

    colors.clear()
    assert len(colors) == 0


def test_colordict_standard_mapping_updates():
    colors = ColorDict()
    colors.update([(1, "red"), ((2, 1), "blue")], accent="lime")

    assert colors[1] == Color.red()
    assert colors[(2, 1)] == Color.blue()
    assert colors["accent"] == Color.green()
    assert 1.5 not in colors


def test_colordict_rejects_none_values():
    colors = ColorDict()

    with pytest.raises(ColorError):
        colors[0] = None


def test_colordict_rejects_invalid_keys():
    colors = ColorDict()

    colors[True] = Color.red()
    colors[(1, "2")] = Color.green()
    colors[1.5] = Color.blue()

    assert colors[True] == Color.red()
    assert colors[(1, "2")] == Color.green()
    assert colors[1.5] == Color.blue()

    with pytest.raises(TypeError, match="unhashable"):
        colors[[1, 2]] = Color.red()


def test_colordict_data_items_rely_on_pair_unpacking():
    with pytest.raises(ValueError):
        ColorDict.__from_data__({"default": Color.black(), "items": [[1]]})
