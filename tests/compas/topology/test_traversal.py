from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.datastructures import Network
from compas.geometry import Box, Frame
from compas.topology import astar_shortest_path
from compas.topology.traversal import astar_lightest_path


def test_astar_shortest_path():
    n = Network()
    a = n.add_node(x=1, y=2, z=0)
    b = n.add_node(x=3, y=1, z=0)
    n.add_edge(a, b)
    path = astar_shortest_path(n, a, b)
    assert path == [a, b]


def test_astar_shortest_path_cycle():
    n = Network()
    a = n.add_node(x=1, y=0, z=0)
    b = n.add_node(x=2, y=0, z=0)
    c = n.add_node(x=3, y=0, z=0)
    d = n.add_node(x=4, y=0, z=0)
    e = n.add_node(x=3.5, y=5, z=0)
    n.add_edge(a, b)
    n.add_edge(a, e)
    n.add_edge(b, c)
    n.add_edge(c, d)
    n.add_edge(e, d)
    path = astar_shortest_path(n, a, d)
    assert path == [a, b, c, d]


def test_astar_shortest_path_disconnected():
    n = Network()
    a = n.add_node(x=1, y=0, z=0)
    b = n.add_node(x=2, y=0, z=0)
    c = n.add_node(x=3, y=0, z=0)
    n.add_edge(a, b)
    path = astar_shortest_path(n, a, c)
    assert path is None


def test_astar_shortest_path_mesh():
    mesh = Mesh.from_shape(Box(Frame.worldXY(), 1, 1, 1))
    a, b = mesh.get_any_vertices(2)
    path = astar_shortest_path(mesh, a, b)
    assert path is not None


def test_astar_lightest_path():
    g = Graph()
    for i in range(4):
        g.add_node(i)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 3)
    weights = {
        (0, 1): 1,
        (0, 2): 1,
        (1, 3): 2,
        (2, 3): 1,
    }
    heuristic = {i: 1 for i in range(4)}
    path = astar_lightest_path(g.adjacency, weights, heuristic, 0, 3)
    assert path == [0, 2, 3]
