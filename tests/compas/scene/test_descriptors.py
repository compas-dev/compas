from compas.colors import Color
from compas.colors import ColorDict
from compas.scene.descriptors.color import ColorAttribute
from compas.scene.descriptors.colordict import ColorDictAttribute


class ColorOwner:
    color = ColorAttribute(Color.red())
    colors = ColorDictAttribute(Color.black())


def test_descriptors_support_class_access():
    assert isinstance(ColorOwner.color, ColorAttribute)
    assert isinstance(ColorOwner.colors, ColorDictAttribute)


def test_color_attribute_coerces_values():
    owner = ColorOwner()

    assert owner.color == Color.red()

    owner.color = (0.0, 1.0, 0.0)

    assert owner.color == Color.green()


def test_colordict_attribute_preserves_colordict_default():
    owner = ColorOwner()
    colors = ColorDict(default=Color.red())
    colors[0] = Color.green()

    owner.colors = colors

    assert owner.colors.default == Color.red()
    assert owner.colors[0] == Color.green()


def test_colordict_attribute_empty_mapping_clears_items():
    owner = ColorOwner()
    owner.colors = {0: Color.red()}

    owner.colors = {}

    assert len(owner.colors) == 0
    assert owner.colors.default == Color.black()
