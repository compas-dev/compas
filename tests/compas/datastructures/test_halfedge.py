import pytest
import random

import compas

from compas.geometry import Sphere
from compas.geometry import Box

from compas.datastructures import HalfEdge
from compas.datastructures import Mesh


# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def mesh():
    vertices = [None, None, None, None]
    faces = [[0, 1, 2], [0, 3, 1]]
    he = HalfEdge()
    for vertex in vertices:
        he.add_vertex()
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


@pytest.fixture
def sphere():
    sphere = Sphere([0, 0, 0], 1.0)
    mesh = Mesh.from_shape(sphere, u=16, v=16)
    return mesh


@pytest.fixture
def box():
    box = Box.from_corner_corner_height([0, 0, 0], [1, 1, 0], 1.0)
    mesh = Mesh.from_shape(box)
    return mesh


@pytest.fixture
def grid():
    mesh = Mesh.from_meshgrid(dx=10, nx=10)
    return mesh


# ==============================================================================
# Tests - Schema & jsonschema
# ==============================================================================


def test_edgedata_nondirectionality(mesh):
    mesh.update_default_edge_attributes({"index": 0})
    for index, (u, v) in enumerate(mesh.edges()):
        mesh.edge_attribute((u, v), "index", index)
    assert all(mesh.edge_attribute((u, v), "index") == mesh.edge_attribute((v, u), "index") for u, v in mesh.edges())


def test_edgedata_io(mesh):
    mesh.update_default_edge_attributes({"index": 0})
    for index, (u, v) in enumerate(mesh.edges()):
        mesh.edge_attribute((u, v), "index", index)
    other = HalfEdge.from_data(mesh.data)
    assert all(other.edge_attribute(edge, "index") == index for index, edge in enumerate(other.edges()))


def test_data_schema(mesh):
    if not compas.IPY:
        mesh.validate_data()


def test_json_schema(mesh):
    if not compas.IPY:
        mesh.validate_json()


# ==============================================================================
# Tests - Samples
# ==============================================================================


def test_vertex_sample(mesh):
    for vertex in mesh.vertex_sample():
        assert mesh.has_vertex(vertex)
    for vertex in mesh.vertex_sample(size=mesh.number_of_vertices()):
        assert mesh.has_vertex(vertex)


def test_edge_sample(mesh):
    for edge in mesh.edge_sample():
        assert mesh.has_edge(edge)
    for edge in mesh.edge_sample(size=mesh.number_of_edges()):
        assert mesh.has_edge(edge)


def test_face_sample(mesh):
    for face in mesh.face_sample():
        assert mesh.has_face(face)
    for face in mesh.face_sample(size=mesh.number_of_faces()):
        assert mesh.has_face(face)


# ==============================================================================
# Tests - Vertex Attributes
# ==============================================================================


def test_default_vertex_attributes():
    he = HalfEdge(name="test", default_vertex_attributes={"a": 1, "b": 2})
    for vertex in he.vertices():
        assert he.vertex_attribute(vertex, name="a") == 1
        assert he.vertex_attribute(vertex, name="b") == 2
        he.vertex_attribute(vertex, name="a", value=3)
        assert he.vertex_attribute(vertex, name="a") == 3


def test_vertex_attributes_key_not_found(mesh):
    with pytest.raises(KeyError):
        mesh.vertex_attributes(mesh.number_of_vertices() + 1)


def test_vertex_attributes_from_defaults(mesh):
    mesh.update_default_vertex_attributes({"foo": "bar"})
    assert mesh.vertex_attributes(mesh.get_any_vertex())["foo"] == "bar"


def test_vertex_attributes_not_in_defaults(mesh):
    mesh.update_default_vertex_attributes({"foo": "bar"})
    attrs = mesh.vertex_attributes(mesh.get_any_vertex())
    with pytest.raises(KeyError):
        attrs["baz"]


def test_get_vertex_attribute_from_view(mesh, vertex_key):
    mesh.vertex_attribute(vertex_key, name="foo", value="bar")
    attrs = mesh.vertex_attributes(vertex_key)
    assert attrs["foo"] == "bar"


def test_set_vertex_attribute_in_view(mesh, vertex_key):
    attrs = mesh.vertex_attributes(vertex_key)
    attrs["foo"] = "bar"
    assert mesh.vertex_attribute(vertex_key, name="foo") == "bar"


def test_del_vertex_attribute_in_view(mesh, vertex_key):
    mesh.vertex_attribute(vertex_key, name="foo", value="bar")
    attrs = mesh.vertex_attributes(vertex_key)
    del attrs["foo"]
    with pytest.raises(KeyError):
        attrs["foo"]


# ==============================================================================
# Tests - Face Attributes
# ==============================================================================


def test_default_face_attributes():
    he = HalfEdge(name="test", default_face_attributes={"a": 1, "b": 2})
    for face in he.vertices():
        assert he.face_attribute(face, name="a") == 1
        assert he.face_attribute(face, name="b") == 2
        he.face_attribute(face, name="a", value=3)
        assert he.face_attribute(face, name="a") == 3


def test_face_attributes_is_empty(mesh):
    assert mesh.face_attributes(mesh.get_any_face()) == {}


def test_face_attributes_from_defaults(mesh):
    mesh.update_default_face_attributes({"foo": "bar"})
    assert mesh.face_attributes(mesh.get_any_face())["foo"] == "bar"


def test_face_attributes_not_in_defaults(mesh):
    mesh.update_default_face_attributes({"foo": "bar"})
    attrs = mesh.face_attributes(mesh.get_any_face())
    with pytest.raises(KeyError):
        attrs["baz"]


def test_get_face_attribute_from_view(mesh, face_key):
    mesh.face_attribute(face_key, name="foo", value="bar")
    attrs = mesh.face_attributes(face_key)
    assert attrs["foo"] == "bar"


def test_set_face_attribute_in_view(mesh, face_key):
    attrs = mesh.face_attributes(face_key)
    attrs["foo"] = "bar"
    assert mesh.face_attribute(face_key, name="foo") == "bar"


def test_del_face_attribute_in_view(mesh, face_key):
    mesh.face_attribute(face_key, name="foo", value="bar")
    attrs = mesh.face_attributes(face_key)
    del attrs["foo"]
    with pytest.raises(KeyError):
        attrs["foo"]


# ==============================================================================
# Tests - Edge Attributes
# ==============================================================================


def test_default_edge_attributes():
    he = HalfEdge(name="test", default_edge_attributes={"a": 1, "b": 2})
    for edge in he.vertices():
        assert he.edge_attribute(edge, name="a") == 1
        assert he.edge_attribute(edge, name="b") == 2
        he.edge_attribute(edge, name="a", value=3)
        assert he.edge_attribute(edge, name="a") == 3


def test_edge_attributes_is_empty(mesh, edge_key):
    assert mesh.edge_attributes(edge_key) == {}


def test_edge_attributes_from_defaults(mesh, edge_key):
    mesh.update_default_edge_attributes({"foo": "bar"})
    assert mesh.edge_attributes(edge_key)["foo"] == "bar"


def test_edge_attributes_not_in_defaults(mesh, edge_key):
    mesh.update_default_edge_attributes({"foo": "bar"})
    attrs = mesh.edge_attributes(edge_key)
    with pytest.raises(KeyError):
        attrs["baz"]


def test_get_edge_attribute_from_view(mesh, edge_key):
    mesh.edge_attribute(edge_key, name="foo", value="bar")
    attrs = mesh.edge_attributes(edge_key)
    assert attrs["foo"] == "bar"


def test_set_edge_attribute_in_view(mesh, edge_key):
    attrs = mesh.edge_attributes(edge_key)
    attrs["foo"] = "bar"
    assert mesh.edge_attribute(edge_key, name="foo") == "bar"


def test_del_edge_attribute_in_view(mesh, edge_key):
    mesh.edge_attribute(edge_key, name="foo", value="bar")
    attrs = mesh.edge_attributes(edge_key)
    del attrs["foo"]
    with pytest.raises(KeyError):
        attrs["foo"]


# ==============================================================================
# Tests - Halfedges Before/After
# ==============================================================================


def test_halfedge_after_on_boundary(grid):
    corners = list(grid.vertices_where(vertex_degree=2))
    corner = corners[0]
    nbrs = grid.vertex_neighbors(corner, ordered=True)
    nbr = nbrs[-1]
    edge = grid.halfedge_after(nbr, corner)
    assert edge[0] == corner
    assert grid.is_edge_on_boundary(*edge)
    assert grid.halfedge_face(*edge) is None


def test_halfedge_before_on_boundary(grid):
    corners = list(grid.vertices_where(vertex_degree=2))
    corner = corners[0]
    nbrs = grid.vertex_neighbors(corner, ordered=True)
    nbr = nbrs[0]
    edge = grid.halfedge_before(corner, nbr)
    assert edge[1] == corner
    assert grid.is_edge_on_boundary(*edge)
    assert grid.halfedge_face(*edge) is None


# ==============================================================================
# Tests - Loops & Strip
# ==============================================================================


def test_loops_and_strips_closed(sphere):
    poles = list(sphere.vertices_where({"vertex_degree": 16}))

    for nbr in sphere.vertex_neighbors(poles[0]):
        meridian = sphere.edge_loop((poles[0], nbr))

        assert len(meridian) == 16, meridian
        assert meridian[0][0] == poles[0]
        assert meridian[-1][1] == poles[1]

        for edge in meridian[1:-1]:
            strip = sphere.edge_strip(edge)

            assert len(strip) == 17, strip
            assert strip[0] == strip[-1]

        for edge in meridian[1:-1]:
            ring = sphere.edge_loop(sphere.halfedge_before(*edge))

            assert len(ring) == 16, ring
            assert ring[0][0] == ring[-1][1]


def test_loops_and_strips_open(grid):
    assert grid.number_of_edges() == 220

    edge = 47, 48
    strip = grid.edge_strip(edge)
    loop = grid.edge_loop(edge)

    assert edge in strip
    assert len(strip) == 11
    assert grid.is_edge_on_boundary(*strip[0])
    assert grid.is_edge_on_boundary(*strip[-1])

    assert edge in loop
    assert len(loop) == 10
    assert grid.is_vertex_on_boundary(loop[0][0])
    assert grid.is_vertex_on_boundary(loop[-1][1])


def test_loops_and_strips_open_corner(grid):
    assert grid.number_of_edges() == 220

    edge = 0, 1
    loop = grid.edge_loop(edge)
    strip = grid.edge_strip(edge)

    assert edge in strip
    assert len(strip) == 11
    assert grid.is_edge_on_boundary(*strip[0])
    assert grid.is_edge_on_boundary(*strip[-1])
    assert edge == strip[-1]

    assert edge in loop
    assert len(loop) == 10
    assert edge == loop[0]

    edge = 1, 0
    loop = grid.edge_loop(edge)
    strip = grid.edge_strip(edge)

    assert edge in strip
    assert len(strip) == 11
    assert grid.is_edge_on_boundary(*strip[0])
    assert grid.is_edge_on_boundary(*strip[-1])
    assert edge == strip[0]

    assert edge in loop
    assert len(loop) == 10
    assert edge == loop[-1]


def test_loops_and_strips_open_boundary(grid):
    assert grid.number_of_edges() == 220

    edge = random.choice(grid.edges_on_boundary())
    u, v = edge

    loop = grid.edge_loop(edge)
    strip = grid.edge_strip(edge)

    assert edge in strip
    assert len(strip) == 11
    assert grid.is_edge_on_boundary(*strip[0])
    assert grid.is_edge_on_boundary(*strip[-1])

    assert edge in loop
    assert len(loop) == 10

    if grid.halfedge[u][v] is None:
        assert edge == strip[-1]
    else:
        assert edge == strip[0]


def test_split_strip_closed(box):
    edge = box.edge_sample()[0]

    box.split_strip(edge)

    assert box.is_valid()
    assert box.number_of_faces() == 10


def test_split_strip_open(grid):
    edge = grid.edge_sample()[0]

    grid.split_strip(edge)

    assert grid.is_valid()
    assert grid.number_of_faces() == 110


def test_split_strip_open_corner(grid):
    corner = list(grid.vertices_where({"vertex_degree": 2}))[0]

    for edge in grid.vertex_edges(corner):
        grid.split_strip(edge)

    assert grid.is_valid()
    assert grid.number_of_faces() == 121


def test_strip_faces_closed(box):
    edge = box.edge_sample()[0]

    strip, faces = box.edge_strip(edge, return_faces=True)

    assert len(strip) == 5
    assert len(faces) == 4
    assert box.edge_faces(*strip[0]) == box.edge_faces(*strip[-1])


def test_strip_faces_open(grid):
    edge = grid.edge_sample()[0]

    strip, faces = grid.edge_strip(edge, return_faces=True)

    assert grid.is_face_on_boundary(faces[0])
    assert grid.is_face_on_boundary(faces[-1])
