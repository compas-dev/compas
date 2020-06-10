import pytest

from compas.datastructures import HalfEdge


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def mesh():
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
        he.add_vertex(x=vertex[0], y=vertex[1], z=vertex[2])

    for face in faces:
        he.add_face(face)

    return he


@pytest.fixture
def vertex_key():
    return 2


@pytest.fixture
def face_key():
    return 1


@pytest.fixture
def edge_key():
    return (0, 1)


# ==============================================================================
# Tests - Vertex Attributes
# ==============================================================================

def test_vertex_attributes_key_not_found(mesh):
    with pytest.raises(KeyError):
        mesh.vertex_attributes(key=mesh.number_of_vertices() + 1)


def test_vertex_attributes_from_defaults(mesh):
    mesh.update_default_vertex_attributes({"foo": "bar"})
    assert mesh.vertex_attributes(key=mesh.get_any_vertex())["foo"] == "bar"


def test_vertex_attributes_not_in_defaults(mesh):
    mesh.update_default_vertex_attributes({"foo": "bar"})
    attrs = mesh.vertex_attributes(key=mesh.get_any_vertex())
    with pytest.raises(KeyError):
        attrs["baz"]


def test_get_vertex_attribute_from_view(mesh, vertex_key):
    mesh.vertex_attribute(key=vertex_key, name="foo", value="bar")
    attrs = mesh.vertex_attributes(key=vertex_key)
    assert attrs["foo"] == "bar"


def test_set_vertex_attribute_in_view(mesh, vertex_key):
    attrs = mesh.vertex_attributes(key=vertex_key)
    attrs["foo"] = "bar"
    assert mesh.vertex_attribute(key=vertex_key, name="foo") == "bar"


def test_del_vertex_attribute_in_view(mesh, vertex_key):
    mesh.vertex_attribute(key=vertex_key, name="foo", value="bar")
    attrs = mesh.vertex_attributes(key=vertex_key)
    del attrs["foo"]
    with pytest.raises(KeyError):
        attrs["foo"]


# ==============================================================================
# Tests - Face Attributes
# ==============================================================================

def test_face_attributes_is_empty(mesh):
    assert mesh.face_attributes(key=mesh.get_any_face()) == {}


def test_face_attributes_from_defaults(mesh):
    mesh.update_default_face_attributes({"foo": "bar"})
    assert mesh.face_attributes(key=mesh.get_any_face())["foo"] == "bar"


def test_face_attributes_not_in_defaults(mesh):
    mesh.update_default_face_attributes({"foo": "bar"})
    attrs = mesh.face_attributes(key=mesh.get_any_face())
    with pytest.raises(KeyError):
        attrs["baz"]


def test_get_face_attribute_from_view(mesh, face_key):
    mesh.face_attribute(key=face_key, name="foo", value="bar")
    attrs = mesh.face_attributes(key=face_key)
    assert attrs["foo"] == "bar"


def test_set_face_attribute_in_view(mesh, face_key):
    attrs = mesh.face_attributes(key=face_key)
    attrs["foo"] = "bar"
    assert mesh.face_attribute(key=face_key, name="foo") == "bar"


def test_del_face_attribute_in_view(mesh, face_key):
    mesh.face_attribute(key=face_key, name="foo", value="bar")
    attrs = mesh.face_attributes(key=face_key)
    del attrs["foo"]
    with pytest.raises(KeyError):
        attrs["foo"]


# ==============================================================================
# Tests - Edge Attributes
# ==============================================================================

def test_edge_attributes_is_empty(mesh, edge_key):
    assert mesh.edge_attributes(key=edge_key) == {}


def test_edge_attributes_from_defaults(mesh, edge_key):
    mesh.update_default_edge_attributes({"foo": "bar"})
    assert mesh.edge_attributes(key=edge_key)["foo"] == "bar"


def test_edge_attributes_not_in_defaults(mesh, edge_key):
    mesh.update_default_edge_attributes({"foo": "bar"})
    attrs = mesh.edge_attributes(key=edge_key)
    with pytest.raises(KeyError):
        attrs["baz"]


def test_get_edge_attribute_from_view(mesh, edge_key):
    mesh.edge_attribute(key=edge_key, name="foo", value="bar")
    attrs = mesh.edge_attributes(key=edge_key)
    assert attrs["foo"] == "bar"


def test_set_edge_attribute_in_view(mesh, edge_key):
    attrs = mesh.edge_attributes(key=edge_key)
    attrs["foo"] = "bar"
    assert mesh.edge_attribute(key=edge_key, name="foo") == "bar"


def test_del_edge_attribute_in_view(mesh, edge_key):
    mesh.edge_attribute(key=edge_key, name="foo", value="bar")
    attrs = mesh.edge_attributes(key=edge_key)
    del attrs["foo"]
    with pytest.raises(KeyError):
        attrs["foo"]
