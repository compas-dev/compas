import pytest

from compas.datastructures.attributes import AttributeView
from compas.datastructures.attributes import CellAttributeView
from compas.datastructures.attributes import EdgeAttributeView
from compas.datastructures.attributes import FaceAttributeView
from compas.datastructures.attributes import NodeAttributeView
from compas.datastructures.attributes import VertexAttributeView


def test_attribute_view_combines_default_and_custom_attributes():
    defaults = {"color": "red", "size": 1}
    custom = {"color": "blue", "name": "custom"}
    view = AttributeView(defaults, custom)

    assert len(view) == 3
    assert dict(view) == {"color": "blue", "size": 1, "name": "custom"}
    assert view["color"] == "blue"
    assert view["size"] == 1


def test_attribute_view_mutates_only_custom_attributes():
    defaults = {"color": "red"}
    custom = {"color": "blue"}
    view = AttributeView(defaults, custom)

    view["size"] = 1
    del view["color"]

    assert custom == {"size": 1}
    assert view["color"] == "red"
    with pytest.raises(KeyError, match="missing"):
        view["missing"]


def test_custom_only_attribute_view_has_consistent_length():
    view = AttributeView({"color": "red", "size": 1}, {"name": "custom"}, custom_only=True)

    assert list(view) == ["name"]
    assert len(view) == 1
    assert dict(view) == {"name": "custom"}
    assert "color" not in view
    with pytest.raises(KeyError, match="color"):
        view["color"]


@pytest.mark.parametrize(
    "view_type",
    [NodeAttributeView, VertexAttributeView, EdgeAttributeView, FaceAttributeView, CellAttributeView],
)
def test_specific_attribute_views_inherit_behavior(view_type):
    custom = {}
    view = view_type({"default": True}, custom)

    view["custom"] = True

    assert dict(view) == {"default": True, "custom": True}
    assert custom == {"custom": True}
