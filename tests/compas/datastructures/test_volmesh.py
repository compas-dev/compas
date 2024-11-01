import pytest
import json
import compas
from compas.datastructures import VolMesh

# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def halfface():
    return VolMesh.from_meshgrid(1, 1, 1, 2, 2, 2)


# ==============================================================================
# Basics
# ==============================================================================

# ==============================================================================
# Constructors
# ==============================================================================

# ==============================================================================
# Data
# ==============================================================================


def test_halfface_data(halfface):
    # type: (VolMesh) -> None
    other = VolMesh.__from_data__(json.loads(json.dumps(halfface.__data__)))

    assert halfface.__data__ == other.__data__
    assert halfface.default_vertex_attributes == other.default_vertex_attributes
    assert halfface.default_edge_attributes == other.default_edge_attributes
    assert halfface.default_face_attributes == other.default_face_attributes
    assert halfface.default_cell_attributes == other.default_cell_attributes
    assert halfface.number_of_vertices() == other.number_of_vertices()
    assert halfface.number_of_edges() == other.number_of_edges()
    assert halfface.number_of_faces() == other.number_of_faces()
    assert halfface.number_of_cells() == other.number_of_cells()

    if not compas.IPY:
        assert VolMesh.validate_data(halfface.__data__)
        assert VolMesh.validate_data(other.__data__)


def test_volmesh_data():
    vmesh = VolMesh.from_obj(compas.get("boxes.obj"))
    other = VolMesh.__from_data__(json.loads(json.dumps(vmesh.__data__)))

    assert vmesh.__data__ == other.__data__
    assert vmesh.number_of_vertices() == other.number_of_vertices()
    assert vmesh.number_of_edges() == other.number_of_edges()
    assert vmesh.number_of_faces() == other.number_of_faces()
    assert vmesh.number_of_cells() == other.number_of_cells()

    if not compas.IPY:
        assert VolMesh.validate_data(vmesh.__data__)
        assert VolMesh.validate_data(other.__data__)


# ==============================================================================
# Builders
# ==============================================================================

# ==============================================================================
# Modifiers
# ==============================================================================

# ==============================================================================
# Samples
# ==============================================================================

# ==============================================================================
# Vertex Attributes
# ==============================================================================


def test_default_vertex_attributes():
    he = VolMesh(name="test", default_vertex_attributes={"a": 1, "b": 2})
    for vertex in he.vertices():
        assert he.vertex_attribute(vertex, name="a") == 1
        assert he.vertex_attribute(vertex, name="b") == 2
        he.vertex_attribute(vertex, name="a", value=3)
        assert he.vertex_attribute(vertex, name="a") == 3


# ==============================================================================
# Face Attributes
# ==============================================================================


def test_default_face_attributes():
    he = VolMesh(name="test", default_face_attributes={"a": 1, "b": 2})
    for face in he.vertices():
        assert he.face_attribute(face, name="a") == 1
        assert he.face_attribute(face, name="b") == 2
        he.face_attribute(face, name="a", value=3)
        assert he.face_attribute(face, name="a") == 3


# ==============================================================================
# Edge Attributes
# ==============================================================================


def test_default_edge_attributes():
    he = VolMesh(name="test", default_edge_attributes={"a": 1, "b": 2})
    for edge in he.vertices():
        assert he.edge_attribute(edge, name="a") == 1
        assert he.edge_attribute(edge, name="b") == 2
        he.edge_attribute(edge, name="a", value=3)
        assert he.edge_attribute(edge, name="a") == 3


# ==============================================================================
# Cell Attributes
# ==============================================================================


def test_default_cell_attributes():
    he = VolMesh(name="test", default_cell_attributes={"a": 1, "b": 2})
    for cell in he.vertices():
        assert he.cell_attribute(cell, name="a") == 1
        assert he.cell_attribute(cell, name="b") == 2
        he.cell_attribute(cell, name="a", value=3)
        assert he.cell_attribute(cell, name="a") == 3


# ==============================================================================
# Vertex Queries
# ==============================================================================


def test_vertices_where():
    hf = VolMesh(default_vertex_attributes={"a": 1, "b": 2})
    hf.add_vertex(0)
    hf.add_vertex(1, {"a": 5})
    hf.add_vertex(2, {"a": 5, "b": 10})
    assert list(hf.vertices_where({"a": 5})) == [1, 2]
    assert list(hf.vertices_where({"a": 1, "b": 2}))[0] == 0


def test_vertices_where_predicate():
    hf = VolMesh(default_vertex_attributes={"a": 1, "b": 2})
    hf.add_vertex(0)
    hf.add_vertex(1, {"a": 5, "b": 10})
    hf.add_vertex(2, {"a": 15, "b": 20})
    assert list(hf.vertices_where_predicate(lambda v, attr: attr["b"] - attr["a"] == 5)) == [1, 2]


# ==============================================================================
# Edge Queries
# ==============================================================================


def test_edges_where():
    hf = VolMesh(default_edge_attributes={"a": 1, "b": 2})
    for vkey in range(3):
        hf.add_vertex(vkey)
    hf.add_halfface([0, 1, 2])
    hf.edge_attribute((0, 1), "a", 5)
    assert list(hf.edges_where({"a": 1})) == [(0, 2), (1, 2)]


def test_edges_where_predicate():
    hf = VolMesh(default_edge_attributes={"a": 1, "b": 2})
    for vkey in range(3):
        hf.add_vertex(vkey)
    hf.add_halfface([0, 1, 2])
    hf.edge_attribute((0, 1), "a", 5)
    assert list(hf.edges_where_predicate(lambda e, attr: attr["a"] - attr["b"] == 3))[0] == (0, 1)


# ==============================================================================
# Face Queries
# ==============================================================================


def test_faces_where():
    hf = VolMesh(default_face_attributes={"a": 1, "b": 2})
    for vkey in range(5):
        hf.add_vertex(vkey)
    for i in range(3):
        hf.add_halfface([i, i + 1, i + 2])
    hf.face_attribute(1, "a", 5)
    assert list(hf.faces_where({"a": 1})) == [0, 2]


def test_faces_where_predicate():
    hf = VolMesh(default_face_attributes={"a": 1, "b": 2})
    for vkey in range(5):
        hf.add_vertex(vkey)
    for i in range(3):
        hf.add_halfface([i, i + 1, i + 2])
    hf.face_attribute(1, "a", 5)
    assert list(hf.faces_where_predicate(lambda e, attr: attr["a"] - attr["b"] == 3))[0] == 1


# ==============================================================================
# Cell Queries
# ==============================================================================


def test_cells_where():
    hf = VolMesh(default_cell_attributes={"a": 1, "b": 2})
    for vkey in range(6):
        hf.add_vertex(vkey)
    for i in range(3):
        hf.add_cell(
            [
                [i, i + 1, i + 2],
                [i, i + 1, i + 3],
                [i + 1, i + 2, i + 3],
                [i + 2, i + 3, i],
            ]
        )
    hf.cell_attribute(1, "a", 5)
    assert list(hf.cells_where({"a": 1})) == [0, 2]


def test_cells_where_predicate():
    hf = VolMesh(default_cell_attributes={"a": 1, "b": 2})
    for vkey in range(6):
        hf.add_vertex(vkey)
    for i in range(3):
        hf.add_cell(
            [
                [i, i + 1, i + 2],
                [i, i + 1, i + 3],
                [i + 1, i + 2, i + 3],
                [i + 2, i + 3, i],
            ]
        )
    hf.cell_attribute(1, "a", 5)
    assert list(hf.cells_where_predicate(lambda e, attr: attr["a"] - attr["b"] == 3))[0] == 1


# ==============================================================================
# Conversion
# ==============================================================================

# ==============================================================================
# Methods
# ==============================================================================


def test_delete_cell_of_volmesh_with_1_1_1():
    volmesh = VolMesh.from_meshgrid(1, 1, 1, 1, 1, 1)
    nov = volmesh.number_of_vertices()
    noe = volmesh.number_of_edges()
    nof = volmesh.number_of_faces()
    noc = volmesh.number_of_cells()

    volmesh.delete_cell(0)

    assert volmesh.number_of_vertices() == nov
    assert volmesh.number_of_cells() == noc - 1
    assert volmesh.number_of_edges() == noe - 12
    assert volmesh.number_of_faces() == nof - 6


@pytest.mark.parametrize(
    "c",
    [0, 1],
)
def test_delete_cell_of_volmesh_with_2_1_1(c):
    volmesh = VolMesh.from_meshgrid(1, 1, 1, 2, 1, 1)
    nov = volmesh.number_of_vertices()
    noe = volmesh.number_of_edges()
    nof = volmesh.number_of_faces()
    noc = volmesh.number_of_cells()

    volmesh.delete_cell(c)

    assert volmesh.number_of_vertices() == nov
    assert volmesh.number_of_cells() == noc - 1
    assert volmesh.number_of_edges() == noe - 8
    assert volmesh.number_of_faces() == nof - 5


@pytest.mark.parametrize(
    "c",
    [0, 1, 2],
)
def test_delete_cell_of_volmesh_with_3_1_1(c):
    volmesh = VolMesh.from_meshgrid(1, 1, 1, 3, 1, 1)
    nov = volmesh.number_of_vertices()
    noe = volmesh.number_of_edges()
    nof = volmesh.number_of_faces()
    noc = volmesh.number_of_cells()

    volmesh.delete_cell(c)

    if c == 0:
        assert volmesh.number_of_vertices() == nov
        assert volmesh.number_of_cells() == noc - 1
        assert volmesh.number_of_edges() == noe - 8
        assert volmesh.number_of_faces() == nof - 5
    elif c == 1:
        assert volmesh.number_of_vertices() == nov
        assert volmesh.number_of_cells() == noc - 1
        assert volmesh.number_of_edges() == noe - 4
        assert volmesh.number_of_faces() == nof - 4
    elif c == 2:
        assert volmesh.number_of_vertices() == nov
        assert volmesh.number_of_cells() == noc - 1
        assert volmesh.number_of_edges() == noe - 8
        assert volmesh.number_of_faces() == nof - 5
