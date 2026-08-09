import pytest
import json
import compas
from compas.datastructures import VolMesh
from compas.geometry import Scale

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


def test_volmesh_data():
    vmesh = VolMesh.from_obj(compas.get("boxes.obj"))
    other = VolMesh.__from_data__(json.loads(json.dumps(vmesh.__data__)))

    assert vmesh.__data__ == other.__data__
    assert vmesh.number_of_vertices() == other.number_of_vertices()
    assert vmesh.number_of_edges() == other.number_of_edges()
    assert vmesh.number_of_faces() == other.number_of_faces()
    assert vmesh.number_of_cells() == other.number_of_cells()


def test_volmesh_data_preserves_cell_attributes():
    volmesh = VolMesh.from_meshgrid(1, nx=2, ny=1, nz=1)
    volmesh.cell_attribute(0, "name", "first")
    volmesh.cell_attribute(1, "name", "second")

    data = json.loads(json.dumps(volmesh.__data__))
    other = VolMesh.__from_data__(data)

    assert other.cell_attribute(0, "name") == "first"
    assert other.cell_attribute(1, "name") == "second"
    assert other.__data__ == data


def test_volmesh_constructors_preserve_subclass():
    class CustomVolMesh(VolMesh):
        pass

    volmesh = CustomVolMesh.from_meshgrid(1, nx=1, ny=1, nz=1)
    other = CustomVolMesh.__from_data__(json.loads(json.dumps(volmesh.__data__)))

    assert type(volmesh) is CustomVolMesh
    assert type(other) is CustomVolMesh


def test_volmesh_vertices_and_cells_roundtrip():
    volmesh = VolMesh.from_meshgrid(1, 2, 3, 2, 1, 1)

    vertices, cells = volmesh.to_vertices_and_cells()
    other = VolMesh.from_vertices_and_cells(vertices, cells)

    assert other.number_of_vertices() == volmesh.number_of_vertices()
    assert other.number_of_edges() == volmesh.number_of_edges()
    assert other.number_of_faces() == volmesh.number_of_faces()
    assert other.number_of_cells() == volmesh.number_of_cells()


def test_volmesh_clear_resets_topology(halfface):
    halfface.clear()

    assert halfface.number_of_vertices() == 0
    assert halfface.number_of_edges() == 0
    assert halfface.number_of_faces() == 0
    assert halfface.number_of_cells() == 0
    assert halfface.__data__["max_vertex"] == -1
    assert halfface.__data__["max_face"] == -1
    assert halfface.__data__["max_cell"] == -1


# ==============================================================================
# Builders
# ==============================================================================


def test_add_halfface_preserves_input_attributes():
    volmesh = VolMesh()
    for vertex in range(3):
        volmesh.add_vertex(vertex, x=vertex)
    attributes = {"name": "triangle"}

    face = volmesh.add_halfface([0, 1, 2], attr_dict=attributes, color="red")

    assert set(volmesh.vertices()) == {0, 1, 2}
    assert volmesh.face_attribute(face, "name") == "triangle"
    assert volmesh.face_attribute(face, "color") == "red"
    assert attributes == {"name": "triangle"}


def test_add_halfface_rejects_missing_vertices():
    volmesh = VolMesh()
    volmesh.add_vertex(0, x=0, y=0, z=0)

    with pytest.raises(ValueError, match=r"not part of the volmesh: \[1, 2\]"):
        volmesh.add_halfface([0, 1, 2])

    assert list(volmesh.vertices()) == [0]
    assert list(volmesh.halffaces()) == []


def test_builders_do_not_mutate_input_attributes():
    volmesh = VolMesh()
    vertex_attributes = {"name": "vertex"}
    cell_attributes = {"name": "cell"}

    volmesh.add_vertex(0, attr_dict=vertex_attributes, color="red")
    for vertex in (1, 2, 3):
        volmesh.add_vertex(vertex)
    volmesh.add_cell(
        [[0, 2, 1], [0, 1, 3], [1, 2, 3], [2, 0, 3]],
        attr_dict=cell_attributes,
        color="blue",
    )

    assert vertex_attributes == {"name": "vertex"}
    assert cell_attributes == {"name": "cell"}


# ==============================================================================
# Modifiers
# ==============================================================================


def test_delete_vertex_removes_vertex_and_incident_cells():
    volmesh = VolMesh.from_meshgrid(1, nx=1, ny=1, nz=1)

    volmesh.delete_vertex(0)

    assert not volmesh.has_vertex(0)
    assert volmesh.number_of_vertices() == 7
    assert volmesh.number_of_edges() == 0
    assert volmesh.number_of_faces() == 0
    assert volmesh.number_of_cells() == 0


# ==============================================================================
# Samples
# ==============================================================================


def test_samples_and_vertex_maps():
    volmesh = VolMesh.from_meshgrid(1, nx=2, ny=1, nz=1)

    assert len(volmesh.vertex_sample(2)) == 2
    assert len(volmesh.edge_sample(2)) == 2
    assert len(volmesh.face_sample(2)) == 2
    assert len(volmesh.cell_sample(2)) == 2
    assert volmesh.vertex_index() == {vertex: index for index, vertex in volmesh.index_vertex().items()}
    assert set(volmesh.vertex_gkey()) == set(volmesh.vertices())
    assert set(volmesh.gkey_vertex().values()) == set(volmesh.vertices())


def test_volmesh_validity_check_is_not_implemented(halfface):
    with pytest.raises(NotImplementedError):
        halfface.is_valid()


# ==============================================================================
# Topology
# ==============================================================================


@pytest.mark.parametrize(
    "nx,ny,nz",
    [
        [1, 1, 1],
        [2, 2, 2],
        [3, 3, 3],
    ],
)
def test_vertex_neighbours(nx, ny, nz):
    volmesh = VolMesh.from_meshgrid(1, 1, 1, nx, ny, nz)

    for vertex in volmesh.vertices():
        count = len(volmesh.vertex_neighbors(vertex))

        if volmesh.is_vertex_on_boundary(vertex):
            assert 2 < count < 6
        else:
            assert count == 6


@pytest.mark.parametrize(
    "nx,ny,nz",
    [
        [1, 1, 1],
        [2, 2, 2],
        [3, 3, 3],
    ],
)
def test_vertex_cells(nx, ny, nz):
    volmesh = VolMesh.from_meshgrid(1, 1, 1, nx, ny, nz)

    for vertex in volmesh.vertices():
        nbrs = len(volmesh.vertex_neighbors(vertex))
        cells = len(volmesh.vertex_cells(vertex))

        if nbrs == 6:
            assert cells == 8
        elif nbrs == 5:
            assert cells == 4
        elif nbrs == 4:
            assert cells == 2
        elif nbrs == 3:
            assert cells == 1


@pytest.mark.parametrize(
    "nx,ny,nz",
    [
        [1, 1, 1],
        [2, 2, 2],
        [3, 3, 3],
    ],
)
def test_edge_cells(nx, ny, nz):
    volmesh = VolMesh.from_meshgrid(1, 1, 1, nx, ny, nz)

    for edge in volmesh.edges():
        cells = len(volmesh.edge_cells(edge))

        if volmesh.is_edge_on_boundary(edge):
            assert 0 < cells < 3
        else:
            assert cells == 4


@pytest.mark.parametrize(
    "nx,ny,nz",
    [
        [1, 1, 1],
        [2, 2, 2],
        [3, 3, 3],
    ],
)
def test_edge_halffaces(nx, ny, nz):
    volmesh = VolMesh.from_meshgrid(1, 1, 1, nx, ny, nz)

    for edge in volmesh.edges():
        faces = len(volmesh.edge_halffaces(edge))

        if volmesh.is_edge_on_boundary(edge):
            assert 0 < faces < 3
        else:
            assert faces == 4


@pytest.mark.parametrize(
    "nx,ny,nz",
    [
        [1, 1, 1],
        [2, 2, 2],
        [3, 3, 3],
    ],
)
def test_halffaces_on_boundary(nx, ny, nz):
    volmesh = VolMesh.from_meshgrid(1, 1, 1, nx, ny, nz)

    count = sum(volmesh.is_halfface_on_boundary(face) for face in volmesh.halffaces())
    assert count == 2 * nx * ny + 2 * ny * nz + 2 * nx * nz


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


def test_vertex_attribute_can_be_set_to_none(halfface):
    vertex = next(iter(halfface.vertices()))

    halfface.vertex_attribute(vertex, "nullable", None)
    halfface.vertices_attribute("other", None, keys=[vertex])

    assert "nullable" in halfface._vertex[vertex]
    assert "other" in halfface._vertex[vertex]
    assert halfface.vertex_attribute(vertex, "nullable") is None
    assert halfface.vertex_attribute(vertex, "other") is None


def test_vertex_attribute_updates_do_not_mutate_inputs(halfface):
    attributes = {"color": "red"}

    halfface.update_default_vertex_attributes(attributes, weight=1.0)

    assert attributes == {"color": "red"}
    assert halfface.default_vertex_attributes["weight"] == 1.0


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


def test_face_attribute_can_be_set_to_none(halfface):
    face = next(iter(halfface.faces()))

    halfface.face_attribute(face, "nullable", None)
    halfface.faces_attribute("other", None, faces=[face])

    assert "nullable" in halfface.face_attributes(face)
    assert "other" in halfface.face_attributes(face)
    assert halfface.face_attribute(face, "nullable") is None
    assert halfface.face_attribute(face, "other") is None


def test_face_attribute_updates_do_not_mutate_inputs(halfface):
    attributes = {"color": "red"}

    halfface.update_default_face_attributes(attributes, weight=1.0)

    assert attributes == {"color": "red"}
    assert halfface.default_face_attributes["weight"] == 1.0


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


def test_edge_attribute_can_be_set_to_none(halfface):
    edge = next(iter(halfface.edges()))

    halfface.edge_attribute(edge, "nullable", None)
    halfface.edges_attribute("other", None, edges=[edge])

    assert "nullable" in halfface.edge_attributes(edge)
    assert "other" in halfface.edge_attributes(edge)
    assert halfface.edge_attribute(edge[::-1], "nullable") is None
    assert halfface.edge_attribute(edge[::-1], "other") is None


def test_edge_attribute_updates_do_not_mutate_inputs(halfface):
    attributes = {"color": "red"}

    halfface.update_default_edge_attributes(attributes, weight=1.0)

    assert attributes == {"color": "red"}
    assert halfface.default_edge_attributes["weight"] == 1.0


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


def test_cell_attribute_can_be_set_to_none(halfface):
    cell = next(iter(halfface.cells()))

    halfface.cell_attribute(cell, "nullable", None)
    halfface.cells_attribute("other", None, cells=[cell])

    assert "nullable" in halfface.cell_attributes(cell)
    assert "other" in halfface.cell_attributes(cell)
    assert halfface.cell_attribute(cell, "nullable") is None
    assert halfface.cell_attribute(cell, "other") is None


def test_cell_attribute_updates_do_not_mutate_inputs(halfface):
    attributes = {"color": "red"}

    halfface.update_default_cell_attributes(attributes, weight=1.0)

    assert attributes == {"color": "red"}
    assert halfface.default_cell_attributes["weight"] == 1.0


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


def test_vertices_where_does_not_mutate_conditions():
    volmesh = VolMesh.from_meshgrid(1, nx=1, ny=1, nz=1)
    conditions = {"x": (0, 0)}

    vertices = list(volmesh.vertices_where(conditions))

    assert len(vertices) == 4
    assert conditions == {"x": (0, 0)}


def test_vertices_where_predicate():
    hf = VolMesh(default_vertex_attributes={"a": 1, "b": 2})
    hf.add_vertex(0)
    hf.add_vertex(1, {"a": 5, "b": 10})
    hf.add_vertex(2, {"a": 15, "b": 20})
    assert list(hf.vertices_where_predicate(lambda v, attr: attr["b"] - attr["a"] == 5)) == [1, 2]


def test_vertex_neighborhood_rejects_nonpositive_ring(halfface):
    vertex = next(iter(halfface.vertices()))

    with pytest.raises(ValueError, match="greater than or equal to 1"):
        halfface.vertex_neighborhood(vertex, ring=0)


def test_vertex_accessors_and_geometry(halfface):
    vertex = next(iter(halfface.vertices()))

    assert len(list(halfface.vertices(data=True))) == halfface.number_of_vertices()
    assert halfface.vertex_degree(vertex) == len(halfface.vertex_neighbors(vertex))
    assert set(halfface.vertex_edges(vertex)) == {(vertex, neighbor) for neighbor in halfface.vertex_neighbors(vertex)}
    assert halfface.vertex_point(vertex) == halfface.vertex_coordinates(vertex)
    assert len(halfface.vertex_laplacian(vertex)) == 3
    assert len(halfface.vertex_neighborhood_centroid(vertex)) == 3


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


def test_edges_where_does_not_mutate_conditions():
    volmesh = VolMesh.from_meshgrid(1, nx=1, ny=1, nz=1)
    conditions = {"edge_length": (0.9, 1.1)}

    edges = list(volmesh.edges_where(conditions))

    assert len(edges) == 12
    assert conditions == {"edge_length": (0.9, 1.1)}


def test_edges_where_predicate():
    hf = VolMesh(default_edge_attributes={"a": 1, "b": 2})
    for vkey in range(3):
        hf.add_vertex(vkey)
    hf.add_halfface([0, 1, 2])
    hf.edge_attribute((0, 1), "a", 5)
    assert list(hf.edges_where_predicate(lambda e, attr: attr["a"] - attr["b"] == 3))[0] == (0, 1)


def test_edge_topology_and_geometry():
    volmesh = VolMesh.from_meshgrid(1, nx=1, ny=1, nz=1)
    edge = next(iter(volmesh.edges()))

    assert volmesh.has_edge(edge)
    assert volmesh.has_edge(edge[::-1])
    assert len(volmesh.edge_halffaces(edge)) == 1
    assert len(volmesh.edge_cells(edge)) == 1
    assert volmesh.is_edge_on_boundary(edge)
    assert volmesh.edge_start(edge) == volmesh.edge_coordinates(edge)[0]
    assert volmesh.edge_end(edge) == volmesh.edge_coordinates(edge)[1]
    assert volmesh.edge_point(edge, 0.5) == volmesh.edge_midpoint(edge)
    assert len(volmesh.edge_vector(edge)) == 3
    assert len(volmesh.edge_direction(edge)) == 3
    assert volmesh.edge_line(edge).length == volmesh.edge_length(edge)


def test_edge_attributes_survive_while_edge_remains():
    volmesh = VolMesh.from_meshgrid(1, nx=2, ny=1, nz=1)
    edge = next(edge for edge in volmesh.edges() if len(volmesh.edge_cells(edge)) == 2)
    volmesh.edge_attribute(edge, "keep", True)

    volmesh.delete_cell(0)

    assert volmesh.has_edge(edge)
    assert volmesh.edge_attribute(edge, "keep") is True

    volmesh.delete_cell(1)

    assert not volmesh.has_edge(edge)
    assert not volmesh._edge_data


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


def test_faces_where_does_not_mutate_conditions():
    volmesh = VolMesh.from_meshgrid(1, nx=2, ny=2, nz=1)
    conditions = {"face_area": (0.2, 0.6)}

    faces = list(volmesh.faces_where(conditions))

    assert faces
    assert conditions == {"face_area": (0.2, 0.6)}


def test_faces_where_predicate():
    hf = VolMesh(default_face_attributes={"a": 1, "b": 2})
    for vkey in range(5):
        hf.add_vertex(vkey)
    for i in range(3):
        hf.add_halfface([i, i + 1, i + 2])
    hf.face_attribute(1, "a", 5)
    assert list(hf.faces_where_predicate(lambda e, attr: attr["a"] - attr["b"] == 3))[0] == 1


def test_halfface_topology_and_face_geometry():
    volmesh = VolMesh.from_meshgrid(1, nx=2, ny=2, nz=1)
    face = next(iter(volmesh.faces()))
    vertices = volmesh.face_vertices(face)

    assert volmesh.has_halfface(face)
    assert volmesh.halfface_vertices(face) == vertices
    assert len(volmesh.halfface_halfedges(face)) == len(vertices)
    assert volmesh.halfface_vertex_ancestor(face, vertices[0]) == vertices[-1]
    assert volmesh.halfface_vertex_descendent(face, vertices[-1]) == vertices[0]
    assert volmesh.halfface_cell(face) is not None
    for halfface in volmesh.halffaces():
        assert all(volmesh.has_halfface(neighbor) for neighbor in volmesh.halfface_manifold_neighbors(halfface))
    assert len(volmesh.face_coordinates(face)) == len(vertices)
    assert len(volmesh.face_points(face)) == len(vertices)
    assert len(volmesh.face_polygon(face).points) == len(vertices)
    assert len(volmesh.face_normal(face)) == 3
    assert len(volmesh.face_centroid(face)) == 3
    assert len(volmesh.face_center(face)) == 3
    assert volmesh.face_area(face) > 0
    assert volmesh.face_flatness(face) == 0
    assert volmesh.face_aspect_ratio(face) >= 1


def test_halfface_manifold_neighbors_support_unattached_halfface():
    volmesh = VolMesh.from_vertices_and_cells([[0, 0, 0], [1, 0, 0], [0, 1, 0]], [])
    face = volmesh.add_halfface([0, 1, 2])

    assert volmesh.halfface_cell(face) is None
    assert volmesh.halfface_manifold_neighbors(face) == []


def test_halfface_manifold_neighborhood_rejects_nonpositive_ring(halfface):
    face = next(iter(halfface.halffaces()))

    with pytest.raises(ValueError, match="greater than or equal to 1"):
        halfface.halfface_manifold_neighborhood(face, ring=0)


def test_face_attributes_survive_while_shared_face_remains():
    volmesh = VolMesh.from_meshgrid(1, nx=2, ny=1, nz=1)
    face = next(face for face in volmesh.faces() if volmesh.halfface_opposite_cell(face) is not None)
    vertices = set(volmesh.face_vertices(face))
    cell = volmesh.halfface_cell(face)
    opposite = volmesh.halfface_opposite_cell(face)
    assert cell is not None and opposite is not None
    volmesh.face_attribute(face, "keep", True)

    volmesh.delete_cell(cell)

    remaining = next(face for face in volmesh.faces() if set(volmesh.face_vertices(face)) == vertices)
    assert volmesh.face_attribute(remaining, "keep") is True

    volmesh.delete_cell(opposite)

    assert all("keep" not in attributes for attributes in volmesh._face_data.values())


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


def test_cells_where_does_not_mutate_conditions():
    volmesh = VolMesh.from_meshgrid(1, nx=2, ny=1, nz=1)
    volmesh.cells_attribute("group", "cell")
    conditions = {"group": "cell"}

    cells = list(volmesh.cells_where(conditions))

    assert cells == list(volmesh.cells())
    assert conditions == {"group": "cell"}


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


def test_cell_topology_and_geometry():
    volmesh = VolMesh.from_meshgrid(3, 1, 1, nx=3, ny=1, nz=1)

    assert [volmesh.cell_neighbors(cell) for cell in volmesh.cells()] == [[1], [2, 0], [1]]
    for cell in volmesh.cells():
        assert volmesh.has_cell(cell)
        assert len(volmesh.cell_vertices(cell)) == 8
        assert len(volmesh.cell_halfedges(cell)) == 24
        assert len(volmesh.cell_edges(cell)) == 12
        assert len(volmesh.cell_faces(cell)) == 6
        for vertex in volmesh.cell_vertices(cell):
            assert len(volmesh.cell_vertex_neighbors(cell, vertex)) == 3
            assert len(volmesh.cell_vertex_faces(cell, vertex)) == 3
        for face in volmesh.cell_faces(cell):
            assert len(volmesh.cell_face_neighbors(cell, face)) == 4

    cell = 0
    vertex = volmesh.cell_vertices(cell)[0]
    assert len(volmesh.cell_points(cell)) == 8
    assert len(volmesh.cell_lines(cell)) == 12
    assert len(volmesh.cell_polygons(cell)) == 6
    assert len(volmesh.cell_centroid(cell)) == 3
    assert len(volmesh.cell_center(cell)) == 3
    assert len(volmesh.cell_vertex_normal(cell, vertex)) == 3
    assert len(volmesh.cell_polyhedron(cell).vertices) == 8


def test_boundary_collections():
    volmesh = VolMesh.from_meshgrid(1, nx=3, ny=3, nz=3)

    assert len(volmesh.vertices_on_boundaries()) == 56
    assert len(volmesh.halffaces_on_boundaries()) == 54
    assert len(volmesh.cells_on_boundaries()) == 26


def test_volmesh_transform():
    volmesh = VolMesh.from_meshgrid(1, nx=1, ny=1, nz=1)
    original = {vertex: volmesh.vertex_coordinates(vertex) for vertex in volmesh.vertices()}

    volmesh.transform(Scale.from_factors([2, 2, 2]))

    for vertex, xyz in original.items():
        assert volmesh.vertex_coordinates(vertex) == [2 * value for value in xyz]


# ==============================================================================
# Conversion
# ==============================================================================


def test_to_points():
    vmesh = VolMesh.from_obj(compas.get("boxes.obj"))
    points = vmesh.to_points()
    assert len(points) == 27


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
