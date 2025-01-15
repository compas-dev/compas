import compas

from compas.colors import Color
from compas.colors import ColorDict


def test_colordict():
    cd = ColorDict(Color.red())
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
    assert cd["1"] == Color.blue()

    assert cd[(1, 0)] == Color.green()
    assert cd["0,1"] == Color.green()

    assert cd["1,0"] == Color.red()


def test_colordict_json():
    cd1 = ColorDict(Color.red())
    cd1[1] = Color.blue()
    cd1[(1, 0)] = Color.green()

    cd2 = compas.json_loads(compas.json_dumps(cd1))

    assert cd2[1] == Color.blue()
    assert cd2["1"] == Color.blue()

    assert cd2[(1, 0)] == Color.green()
    assert cd2["0,1"] == Color.green()

    assert cd2["1,0"] == Color.red()
