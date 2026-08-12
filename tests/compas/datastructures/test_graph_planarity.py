import networkx

from compas.datastructures import Graph


def crossing_graph():
    graph = Graph()
    graph.add_node(0, x=0.0, y=0.0, z=0.0)
    graph.add_node(1, x=1.0, y=1.0, z=0.0)
    graph.add_node(2, x=0.0, y=1.0, z=0.0)
    graph.add_node(3, x=1.0, y=0.0, z=0.0)
    graph.add_edge(0, 1)
    graph.add_edge(2, 3)
    return graph


def square_graph():
    graph = Graph()
    graph.add_node(0, x=0.0, y=0.0, z=0.0)
    graph.add_node(1, x=1.0, y=0.0, z=0.0)
    graph.add_node(2, x=1.0, y=1.0, z=0.0)
    graph.add_node(3, x=0.0, y=1.0, z=0.0)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 0)
    return graph


def test_is_crossed():
    assert crossing_graph().is_crossed()
    assert not square_graph().is_crossed()


def test_find_crossings():
    graph = crossing_graph()

    crossings = graph.find_crossings()

    assert len(crossings) == 1
    assert {frozenset(edge) for edge in crossings[0]} == {frozenset((0, 1)), frozenset((2, 3))}


def test_count_crossings():
    assert crossing_graph().count_crossings() == 1
    assert square_graph().count_crossings() == 0


def test_edges_with_shared_node_do_not_cross():
    graph = Graph()
    graph.add_node(0, x=0.0, y=0.0)
    graph.add_node(1, x=1.0, y=1.0)
    graph.add_node(2, x=2.0, y=0.0)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)

    assert not graph.is_crossed()
    assert graph.find_crossings() == []


def test_is_xy_empty_graph():
    assert Graph().is_xy()


def test_is_xy_with_default_coordinates():
    graph = Graph.from_edges([(0, 1)])

    assert graph.is_xy()


def test_is_xy_constant_elevation():
    graph = Graph()
    graph.add_node(0, z=5.0)
    graph.add_node(1, z=5.0)

    assert graph.is_xy()


def test_is_xy_different_elevations():
    graph = Graph()
    graph.add_node(0, z=0.0)
    graph.add_node(1, z=1.0)

    assert not graph.is_xy()


def test_is_planar_embedding():
    assert square_graph().is_planar_embedding()
    assert not crossing_graph().is_planar_embedding()


def test_embed_in_plane_empty_graph():
    assert not Graph().embed_in_plane()


def test_embed_in_plane(monkeypatch):
    graph = square_graph()
    positions = {
        0: [0.0, 0.0],
        1: [2.0, 0.0],
        2: [2.0, 2.0],
        3: [0.0, 2.0],
    }
    monkeypatch.setattr(networkx, "spring_layout", lambda *args, **kwargs: positions)

    assert graph.embed_in_plane()
    assert graph.node_attributes(0, "xy") == [0.0, 0.0]
    assert graph.node_attributes(2, "xy") == [2.0, 2.0]


def test_embed_in_plane_with_fixed_nodes(monkeypatch):
    graph = square_graph()
    positions = {
        0: [0.0, 0.0],
        1: [2.0, 0.0],
        2: [2.0, 2.0],
        3: [0.0, 2.0],
    }
    monkeypatch.setattr(networkx, "spring_layout", lambda *args, **kwargs: positions)

    assert graph.embed_in_plane(fixed=[0, 1])
    assert graph.node_attributes(0, "xy") == [0.0, 0.0]
    assert graph.node_attributes(1, "xy") == [1.0, 0.0]
