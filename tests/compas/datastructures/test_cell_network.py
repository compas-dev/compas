import pytest
from compas.datastructures import CellNetwork
from compas.geometry import Point


@pytest.fixture
def example_cell_network():
    network = CellNetwork()

    vertices = [
        Point(0, 0, 0),
        Point(0, 1, 0),
        Point(1, 1, 0),
        Point(1, 0, 0),
        Point(0, 0, 1),
        Point(1, 0, 1),
        Point(1, 1, 1),
        Point(0, 1, 1),
        Point(0, 0, 2),
        Point(0, 1, 2),
        Point(1, 1, 2),
        Point(1, 0, 2),
        Point(2, 1, 1),
        Point(2, 0, 1),
        Point(2, 1, 0),
        Point(2, 0, 0),
    ]
    edges = [
        (12, 14),
        (13, 15),
    ]
    faces = [
        [0, 1, 2, 3],
        [0, 3, 5, 4],
        [3, 2, 6, 5],
        [2, 1, 7, 6],
        [1, 0, 4, 7],
        [4, 5, 6, 7],
        [4, 5, 11, 8],
        [7, 4, 8, 9],
        [6, 7, 9, 10],
        [5, 6, 10, 11],
        [8, 9, 10, 11],
        [6, 5, 13, 12],
    ]
    cells = [[0, 1, 2, 3, 4, 5], [5, 6, 7, 8, 9, 10]]

    [network.add_vertex(x=x, y=y, z=z) for x, y, z in vertices]
    [network.add_edge(u, v) for u, v in edges]
    [network.add_face(fverts) for fverts in faces]
    [network.add_cell(fkeys) for fkeys in cells]
    return network


def test_cell_network_data(example_cell_network):
    ds = example_cell_network

    nv = ds.number_of_vertices()
    ne = ds.number_of_edges()
    nf = ds.number_of_faces()
    nc = ds.number_of_cells()

    ds.cell_attribute(1, "heated", True)
    ds.edge_attribute((12, 14), "column", True)
    ds.face_attribute(11, "canopy", True)

    other = CellNetwork.__from_data__(ds.__data__)

    assert other.__data__ == ds.__data__
    assert other.number_of_vertices() is nv
    assert other.number_of_edges() is ne
    assert other.number_of_faces() is nf
    assert other.number_of_cells() is nc

    assert other.cell_attribute(1, "heated") is True
    assert other.edge_attribute((12, 14), "column") is True
    assert other.face_attribute(11, "canopy") is True


def test_cell_network_data_preserves_subclass(example_cell_network):
    class CustomCellNetwork(CellNetwork):
        pass

    other = CustomCellNetwork.__from_data__(example_cell_network.__data__)

    assert type(other) is CustomCellNetwork
    assert other.__data__ == example_cell_network.__data__


def test_cell_network_clear_resets_all_data(example_cell_network):
    network = example_cell_network
    assert network._edge_data

    network.clear()

    assert network.number_of_vertices() == 0
    assert network.number_of_edges() == 0
    assert network.number_of_faces() == 0
    assert network.number_of_cells() == 0
    assert not network._edge_data
    assert network.__data__["max_vertex"] == -1
    assert network.__data__["max_face"] == -1
    assert network.__data__["max_cell"] == -1


def test_cell_network_samples_and_vertex_maps(example_cell_network):
    network = example_cell_network

    assert len(network.vertex_sample(2)) == 2
    assert len(network.edge_sample(2)) == 2
    assert len(network.face_sample(2)) == 2
    assert len(network.cell_sample(2)) == 2
    assert network.vertex_index() == {vertex: index for index, vertex in network.index_vertex().items()}
    assert set(network.vertex_gkey()) == set(network.vertices())
    assert set(network.gkey_vertex().values()) == set(network.vertices())


def test_cell_network_builders_do_not_mutate_input_attributes():
    network = CellNetwork()
    vertex_attributes = {"name": "vertex"}
    edge_attributes = {"name": "edge"}
    face_attributes = {"name": "face"}
    for vertex in range(3):
        network.add_vertex(vertex, attr_dict=vertex_attributes if vertex == 0 else None)

    network.add_edge(0, 1, attr_dict=edge_attributes, color="red")
    network.add_face([0, 1, 2], attr_dict=face_attributes, color="blue")

    assert vertex_attributes == {"name": "vertex"}
    assert edge_attributes == {"name": "edge"}
    assert face_attributes == {"name": "face"}


def test_add_face_rejects_missing_vertices_without_modifying_network():
    network = CellNetwork()
    network.add_vertex(0, x=0, y=0, z=0)

    with pytest.raises(ValueError, match=r"not part of the cell network: \[1, 2\]"):
        network.add_face([0, 1, 2])

    assert list(network.vertices()) == [0]
    assert list(network.edges()) == []
    assert list(network.faces()) == []


def test_add_face_rejects_fewer_than_three_vertices():
    network = CellNetwork()
    network.add_vertex(0)
    network.add_vertex(1)

    with pytest.raises(ValueError, match="at least 3 vertices"):
        network.add_face([0, 1])


def test_delete_edge_removes_edge_attributes():
    network = CellNetwork()
    network.add_vertex(0)
    network.add_vertex(1)
    edge = network.add_edge(0, 1, label="edge")
    key = tuple(sorted(edge))

    network.delete_edge(edge)

    assert not network.has_edge(edge)
    assert key not in network._edge_data


def test_cell_network_conversions(example_cell_network):
    network = example_cell_network

    assert network.edges_to_graph().number_of_edges() == network.number_of_edges()
    assert network.cells_to_graph().number_of_nodes() == network.number_of_cells()
    vertices, faces = network.cell_to_vertices_and_faces(0)
    mesh = network.cell_to_mesh(0)
    assert mesh.number_of_vertices() == len(vertices)
    assert mesh.number_of_faces() == len(faces)
    assert mesh.is_closed()
    assert network.faces_to_mesh(network.faces()).number_of_faces() == network.number_of_faces()


def test_cell_network_vertex_attributes_support_none_and_empty_selection(example_cell_network):
    network = example_cell_network
    network.vertex_attribute(0, "nullable", None)

    assert network.vertex_attribute(0, "nullable") is None
    assert network.vertices_attribute("nullable", keys=[]) == []

    network.vertices_attribute("selected", True, keys=[])
    assert all(network.vertex_attribute(vertex, "selected") is None for vertex in network.vertices())


def test_cell_network_vertex_attribute_inputs_are_not_mutated():
    network = CellNetwork()
    attributes = {"color": "red"}

    network.update_default_vertex_attributes(attributes, size=1)

    assert attributes == {"color": "red"}


def test_cell_network_vertex_neighborhood_rejects_invalid_ring(example_cell_network):
    with pytest.raises(ValueError, match="at least 1"):
        example_cell_network.vertex_neighborhood(0, ring=0)


def test_cell_network_vertex_queries(example_cell_network):
    network = example_cell_network
    network.vertex_attribute(0, "group", "support")
    network.vertex_attribute(0, "tags", ["selected"])
    network.vertex_attribute(1, "tags", ["selected"])

    assert list(network.vertices_where({"group": "support"})) == [0]
    assert list(network.vertices_where({"tags": "selected", "group": "support"})) == [0]
    assert list(network.vertices_where_predicate(lambda vertex, attr: vertex == 0)) == [0]
    assert isinstance(network.vertex_neighbors(0), list)
    assert network.vertex_degree(0) == len(network.vertex_neighbors(0))
    assert network.vertex_point(0) == Point(*network.vertex_coordinates(0))


def test_cell_network_edge_attributes_support_none_and_empty_selection(example_cell_network):
    network = example_cell_network
    edge = next(network.edges())
    network.edge_attribute(edge, "nullable", None)

    assert network.edge_attribute(edge, "nullable") is None
    assert network.edges_attribute("nullable", edges=[]) == []

    network.edges_attribute("selected", True, edges=[])
    assert all(network.edge_attribute(item, "selected") is None for item in network.edges())


def test_cell_network_edge_attribute_inputs_are_not_mutated():
    network = CellNetwork()
    attributes = {"color": "red"}

    network.update_default_edge_attributes(attributes, size=1)

    assert attributes == {"color": "red"}


def test_cell_network_edge_queries_and_geometry(example_cell_network):
    network = example_cell_network
    edge = next(network.edges())
    network.edge_attributes(edge, ["tags", "group"], [["selected"], "frame"])

    assert list(network.edges_where({"tags": "selected", "group": "frame"})) == [edge]
    assert list(network.edges_where_predicate(lambda item, attr: item == edge)) == [edge]
    assert network.edge_midpoint(edge) == network.edge_point(edge)
    assert network.edge_line(edge).length == network.edge_length(edge)


def test_cell_network_edge_cells_are_independent_of_edge_direction(example_cell_network):
    network = example_cell_network

    for edge in network.edges():
        assert set(network.edge_cells(edge)) == set(network.edge_cells(edge[::-1]))


def test_cell_network_face_attributes_support_none_and_empty_selection(example_cell_network):
    network = example_cell_network
    face = next(network.faces())
    network.face_attribute(face, "nullable", None)

    assert network.face_attribute(face, "nullable") is None
    assert network.faces_attribute("nullable", faces=[]) == []

    network.faces_attribute("selected", True, faces=[])
    assert all(network.face_attribute(item, "selected") is None for item in network.faces())


def test_cell_network_face_attribute_inputs_are_not_mutated():
    network = CellNetwork()
    attributes = {"color": "red"}

    network.update_default_face_attributes(attributes, size=1)

    assert attributes == {"color": "red"}


def test_cell_network_face_queries_and_geometry(example_cell_network):
    network = example_cell_network
    face = next(network.faces())
    network.face_attributes(face, ["tags", "group"], [["selected"], "wall"])

    assert list(network.faces_where({"tags": "selected", "group": "wall"})) == [face]
    assert list(network.faces_where_predicate(lambda item, attr: item == face)) == [face]
    assert network.face_polygon(face).area == network.face_area(face)
    assert network.face_plane(face).point == network.face_centroid(face)
    assert len(network.face_edges(face)) == len(network.face_vertices(face))


def test_cell_network_cell_attributes_support_none_and_empty_selection(example_cell_network):
    network = example_cell_network
    cell = next(network.cells())
    network.cell_attribute(cell, "nullable", None)

    assert network.cell_attribute(cell, "nullable") is None
    assert network.cells_attribute("nullable", cells=[]) == []

    network.cells_attribute("selected", True, cells=[])
    assert all(network.cell_attribute(item, "selected") is None for item in network.cells())


def test_cell_network_cell_attribute_inputs_are_not_mutated():
    network = CellNetwork()
    attributes = {"color": "red"}

    network.update_default_cell_attributes(attributes, size=1)

    assert attributes == {"color": "red"}


def test_cell_network_cell_topology(example_cell_network):
    network = example_cell_network
    cell = next(network.cells())

    assert network.has_cell(cell)
    assert not network.has_cell(100)
    assert len(network.cell_edges(cell)) * 2 == len(network.cell_halfedges(cell))
    for vertex in network.cell_vertices(cell):
        assert set(network.cell_vertex_neighbors(cell, vertex)) == set(network.vertex_neighbors(vertex)) & set(
            network.cell_vertices(cell)
        )
    for face in network.cell_faces(cell):
        assert len(network.cell_face_neighbors(cell, face)) == len(network.face_edges(face))


def test_cell_network_cell_queries_and_geometry(example_cell_network):
    network = example_cell_network
    cell = next(network.cells())
    network.cell_attributes(cell, ["tags", "group"], [["selected"], "volume"])

    assert list(network.cells_where({"tags": "selected", "group": "volume"})) == [cell]
    assert list(network.cells_where_predicate(lambda item, attr: item == cell)) == [cell]
    assert len(network.cell_polyhedron(cell).vertices) == len(network.cell_vertices(cell))
    assert network.cell_volume(cell) > 0
    assert len(network.cell_points(cell)) == len(network.cell_vertices(cell))


def test_cell_network_boundary(example_cell_network):
    ds = example_cell_network
    assert set(ds.cells_on_boundaries()) == {0, 1}
    assert set(ds.faces_on_boundaries()) == {0, 1, 2, 3, 4, 6, 7, 8, 9, 10}
    assert set(ds.faces_without_cell()) == {11}
    assert set(ds.edges_without_face()) == {(13, 15), (12, 14)}
    assert set(ds.nonmanifold_edges()) == {(6, 7), (4, 5), (5, 6), (4, 7)}


# ==============================================================================
# Conversion
# ==============================================================================


def test_vertices_to_points(example_cell_network):
    ds = example_cell_network
    points = ds.vertices_to_points()
    assert len(points) == ds.number_of_vertices()
