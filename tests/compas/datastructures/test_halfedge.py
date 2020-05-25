import pytest

from compas.datastructures.mesh.core import HalfEdge


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def halfedge():
    vertices = [
        [1.0, 0.0, 0.0],
        [1.0, 2.0, 0.0],
        [0.0, 1.0, 0.0],
        [2.0, 1.0, 0.0]
    ]

    faces = [
        [0, 1, 2],
        [0, 3, 1]
    ]

    he = HalfEdge()

    for vertex in vertices:
        he.add_vertex(attr_dict={c: xyz for c, xyz in zip("xyz", vertex)})

    for face in faces:
        he.add_face(face)

    return he

@pytest.fixture
def halfedge_default_attrs(halfedge, default_kwattr):
    halfedge.update_default_vertex_attributes(default_kwattr)
    halfedge.update_default_face_attributes(default_kwattr)
    halfedge.update_default_edge_attributes(default_kwattr)
    return halfedge


@pytest.fixture
def default_kwattr():
    return {"foo": "bar"}


@pytest.fixture
def custom_kwattr():
    return {"moo": "baz", 0: "0", "1": 1}


def iterators():
    return ["vertices", "faces", "edges"]

# ==============================================================================
# Tests - Custom Attributes
# ==============================================================================

def test_set_vertex_attribute_custom(halfedge, custom_kwattr):
    key = halfedge.get_any_vertex()
    for name, value in custom_kwattr.items():
        halfedge.vertex_attribute(key=key, name=name, value=value)
        assert name in halfedge.vertex_attributes(key=key)


def test_set_face_attribute_custom(halfedge, custom_kwattr):
    key = halfedge.get_any_face()
    for name, value in custom_kwattr.items():
        halfedge.face_attribute(key=key, name=name, value=value)
        assert name in halfedge.face_attributes(key=key)


def test_set_edge_attribute_custom(halfedge, custom_kwattr):
    key = (0, 1)
    for name, value in custom_kwattr.items():
        halfedge.edge_attribute(key=key, name=name, value=value)
        assert name in halfedge.edge_attributes(key=key)

# ==============================================================================
# Tests - Default Attributes
# ==============================================================================

@pytest.mark.parametrize("iterator", iterators())
def test_get_vertex_attribute_default(halfedge_default_attrs, default_kwattr, iterator):
    for vkey, attr in getattr(halfedge_default_attrs, iterator)(True):
        for k, v in default_kwattr.items():
            assert k in attr


@pytest.mark.parametrize("iterator", iterators())
def test_get_vertex_attribute_not_in_default(halfedge_default_attrs, custom_kwattr, iterator):
    with pytest.raises(KeyError):
        for vkey, attr in getattr(halfedge_default_attrs, iterator)(True):
            for k, v in custom_kwattr.items():
                _ = attr[k]
