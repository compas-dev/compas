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

    assert other.number_of_vertices() is nv
    assert other.number_of_edges() is ne
    assert other.number_of_faces() is nf
    assert other.number_of_cells() is nc

    assert other.cell_attribute(1, "heated") is True
    assert other.edge_attribute((12, 14), "column") is True
    assert other.face_attribute(11, "canopy") is True


def test_cell_network_boundary(example_cell_network):
    ds = example_cell_network
    assert set(ds.cells_on_boundaries()) == {0, 1}
    assert set(ds.faces_on_boundaries()) == {0, 1, 2, 3, 4, 6, 7, 8, 9, 10}
    assert set(ds.faces_without_cell()) == {11}
    assert set(ds.edges_without_face()) == {(15, 13), (14, 12)}
    assert set(ds.nonmanifold_edges()) == {(6, 7), (4, 5), (5, 6), (7, 4)}
