import pytest

from compas.datastructures import Graph


def three_node_graph():
    graph = Graph()
    graph.add_node(0, x=0.0, y=0.0, z=0.0)
    graph.add_node(1, x=1.0, y=1.0, z=0.0)
    graph.add_node(2, x=2.0, y=0.0, z=0.0)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    return graph


def test_smooth_centroid():
    graph = three_node_graph()

    graph.smooth(fixed=[0, 2], kmax=1, damping=1.0)

    assert graph.node_coordinates(1) == [1.0, 0.0, 0.0]


def test_smooth_centroid_with_damping():
    graph = three_node_graph()

    graph.smooth(fixed=[0, 2], kmax=1, damping=0.25)

    assert graph.node_coordinates(1) == [1.0, 0.75, 0.0]


def test_smooth_centroid_fixed_nodes():
    graph = three_node_graph()
    before = {key: graph.node_coordinates(key) for key in graph.nodes()}

    graph.smooth(fixed=graph.nodes(), kmax=3)

    assert {key: graph.node_coordinates(key) for key in graph.nodes()} == before


def test_smooth_centroid_zero_iterations():
    graph = three_node_graph()
    before = {key: graph.node_coordinates(key) for key in graph.nodes()}

    graph.smooth(kmax=0)

    assert {key: graph.node_coordinates(key) for key in graph.nodes()} == before


def test_smooth_centroid_uses_iteration_snapshot():
    graph = Graph()
    graph.add_node(0, x=0.0, y=0.0, z=0.0)
    graph.add_node(1, x=0.0, y=0.0, z=0.0)
    graph.add_node(2, x=3.0, y=0.0, z=0.0)
    graph.add_node(3, x=4.0, y=0.0, z=0.0)
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)

    graph.smooth(fixed=[0, 3], kmax=1, damping=1.0)

    assert graph.node_coordinates(1) == [1.5, 0.0, 0.0]
    assert graph.node_coordinates(2) == [2.0, 0.0, 0.0]


def test_smooth_centroid_isolated_node():
    graph = Graph()
    graph.add_node(0, x=1.0, y=2.0, z=3.0)

    graph.smooth(kmax=1)

    assert graph.node_coordinates(0) == [1.0, 2.0, 3.0]


def test_smooth_centroid_callback():
    graph = three_node_graph()
    calls = []
    callback_args = {"name": "test"}

    def callback(iteration, args):
        calls.append((iteration, args))

    graph.smooth(kmax=3, callback=callback, callback_args=callback_args)

    assert calls == [(0, callback_args), (1, callback_args), (2, callback_args)]


def test_smooth_centroid_invalid_callback():
    graph = three_node_graph()

    with pytest.raises(TypeError):
        graph.smooth(callback="not callable")
