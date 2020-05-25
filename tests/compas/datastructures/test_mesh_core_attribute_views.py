import pytest

from compas.datastructures.mesh.core import VertexAttributeView
from compas.datastructures.mesh.core import EdgeAttributeView
from compas.datastructures.mesh.core import FaceAttributeView

# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def default_attrs():
    return {"0": 0, 1: "1"}


@pytest.fixture
def custom_attrs():
    return {"2": 2, 3: "3"}


@pytest.fixture
def test_attrs():
    return {"foo": "bar"}


@pytest.fixture
def empty_attrs():
    return {}


def view_key():
    return {FaceAttributeView: 0, EdgeAttributeView: (0, 1), VertexAttributeView: 2}

# ==============================================================================
# Tests
# ==============================================================================

@pytest.mark.parametrize(("View", "key"), list(view_key().items()))
def test_get_attribute_in_defaults(View, key, empty_attrs, default_attrs):
    view = View(defaults=default_attrs, attr=empty_attrs, key=key)
    
    for k in default_attrs.keys():
        assert default_attrs[k] == view[k]


@pytest.mark.parametrize(("View", "key"), list(view_key().items()))
def test_get_attributes_in_custom(View, key, empty_attrs, custom_attrs):
    view = View(defaults=empty_attrs, attr={key: custom_attrs}, key=key)
    
    for k in custom_attrs.keys():
        assert custom_attrs[k] == view[k]


@pytest.mark.parametrize(("View", "key"), list(view_key().items()))
def test_get_attributes_in_defaults_raises_exeption(View, key, empty_attrs, default_attrs, test_attrs):
    view = View(defaults=default_attrs, attr=empty_attrs, key=key)
    
    with pytest.raises(KeyError):
        for k in test_attrs.keys():
            _ = view[k]


@pytest.mark.parametrize(("View", "key"), list(view_key().items()))
def test_get_attributes_in_custom_raises_exeption(View, key, empty_attrs, custom_attrs, test_attrs):
    view = View(defaults=empty_attrs, attr=custom_attrs, key=key)
    
    with pytest.raises(KeyError):
        for k in custom_attrs.keys():
            _ = view[k]


@pytest.mark.parametrize(("View", "key"), list(view_key().items()))
def test_del_attributes(View, key, empty_attrs, custom_attrs):
    view = View(defaults=empty_attrs, attr={key: custom_attrs}, key=key)
    
    lenstart = len(custom_attrs)
    k = next(iter(custom_attrs))
    del view[k]

    assert k not in view.attr[key]
    assert len(custom_attrs) == lenstart - 1
    assert len(view.attr) == lenstart - 1


@pytest.mark.parametrize(("View", "key"), list(view_key().items()))
def test_iter_attributes_custom_only(View, key, empty_attrs, custom_attrs, default_attrs):
    view = View(defaults=empty_attrs, attr={key: custom_attrs}, key=key, custom_only=True)

    for name in view:
        assert name not in default_attrs


@pytest.mark.parametrize(("View", "key"), list(view_key().items()))
def test_iter_attributes_custom_only(View, key, empty_attrs, custom_attrs, default_attrs):
    view = View(defaults=empty_attrs, attr={key: custom_attrs}, key=key, custom_only=False)

    for name in view:
        if name in default_attrs:
            assert name in default_attrs
            continue
        assert name in custom_attrs
