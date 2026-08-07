import pytest

from compas.datastructures import Graph
from compas.datastructures.graph.operations.join import graph_polylines


def line_graph(points):
    return Graph.from_lines(list(zip(points, points[1:])))


def normalized_polyline(polyline):
    points = tuple(tuple(point) for point in polyline)
    reverse = tuple(reversed(points))
    return min(points, reverse)


def normalized_polylines(polylines):
    return sorted(normalized_polyline(polyline) for polyline in polylines)


def test_split_edge():
    graph = line_graph([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
    edge = next(graph.edges())

    node = graph.split_edge(edge)

    assert node in graph.node
    assert graph.node_coordinates(node) == [1.0, 0.0, 0.0]
    assert not graph.has_edge(edge)
    assert graph.has_edge((edge[0], node))
    assert graph.has_edge((node, edge[1]))
    assert graph.number_of_nodes() == 3
    assert graph.number_of_edges() == 2


def test_split_edge_at_parameter():
    graph = line_graph([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]])

    node = graph.split_edge(next(graph.edges()), t=0.25)

    assert graph.node_coordinates(node) == [0.5, 0.0, 0.0]


@pytest.mark.parametrize("t", [0.0, -0.1, 1.0, 1.1])
def test_split_edge_invalid_parameter(t):
    graph = line_graph([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])

    with pytest.raises(ValueError):
        graph.split_edge(next(graph.edges()), t=t)


def test_split_edge_missing():
    graph = Graph.from_edges([(0, 1)])
    data = graph.__data__

    node = graph.split_edge((1, 2))

    assert node is None
    assert graph.__data__ == data


def test_split_edge_reverse_direction_is_missing():
    graph = Graph.from_edges([(0, 1)])

    node = graph.split_edge((1, 0))

    assert node is None
    assert list(graph.edges()) == [(0, 1)]


def test_split_edge_uses_default_attributes():
    graph = Graph(default_edge_attributes={"color": "red"})
    graph.add_node(0, x=0.0, y=0.0, z=0.0)
    graph.add_node(1, x=2.0, y=0.0, z=0.0)
    graph.add_edge(0, 1, color="blue")

    node = graph.split_edge((0, 1))

    assert graph.edge_attribute((0, node), "color") == "red"
    assert graph.edge_attribute((node, 1), "color") == "red"


def test_join_edges():
    graph = Graph.from_edges([(0, 1), (1, 2)])

    graph.join_edges(1)

    assert set(graph.nodes()) == {0, 2}
    assert graph.has_edge((0, 2))
    assert graph.number_of_edges() == 1
    assert graph.neighbors(0) == [2]
    assert graph.neighbors(2) == [0]


@pytest.mark.parametrize("key", [0, 3])
def test_join_edges_requires_degree_two(key):
    graph = Graph.from_edges([(0, 1), (1, 2), (1, 3)])
    data = graph.__data__

    graph.join_edges(key)

    assert graph.__data__ == data


def test_join_edges_missing_node():
    graph = Graph.from_edges([(0, 1)])

    with pytest.raises(KeyError):
        graph.join_edges(2)


def test_join_edges_uses_default_attributes():
    graph = Graph(default_edge_attributes={"color": "red"})
    graph.add_edge(0, 1, color="blue")
    graph.add_edge(1, 2, color="green")

    graph.join_edges(1)

    assert graph.edge_attribute((0, 2), "color") == "red"


def test_join_edges_preserves_remaining_node_attributes():
    graph = Graph()
    graph.add_node(0, label="start")
    graph.add_node(1, label="middle")
    graph.add_node(2, label="end")
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)

    graph.join_edges(1)

    assert graph.node_attribute(0, "label") == "start"
    assert graph.node_attribute(2, "label") == "end"


def test_graph_polylines_empty_graph():
    assert graph_polylines(Graph()) == []


def test_graph_polylines_single_edge():
    graph = line_graph([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])

    assert normalized_polylines(graph_polylines(graph)) == [
        ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
    ]


def test_graph_polylines_open_polyline():
    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]]
    graph = line_graph(points)

    assert normalized_polylines(graph_polylines(graph)) == [tuple(tuple(point) for point in points)]


def test_graph_polylines_disconnected():
    graph = Graph.from_lines(
        [
            ([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]),
            ([2.0, 0.0, 0.0], [3.0, 0.0, 0.0]),
        ]
    )

    assert normalized_polylines(graph_polylines(graph)) == [
        ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
        ((2.0, 0.0, 0.0), (3.0, 0.0, 0.0)),
    ]


def test_graph_polylines_branch():
    center = [0.0, 0.0, 0.0]
    endpoints = [[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    graph = Graph.from_lines([(center, endpoint) for endpoint in endpoints])

    polylines = graph_polylines(graph)

    assert len(polylines) == 3
    assert all(len(polyline) == 2 for polyline in polylines)


def test_graph_polylines_closed_cycle():
    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
    graph = Graph.from_lines(list(zip(points, points[1:] + points[:1])))

    polylines = graph_polylines(graph)

    assert len(polylines) == 1
    assert len(polylines[0]) == 5
    assert polylines[0][0] == polylines[0][-1]
    assert {tuple(point) for point in polylines[0]} == {tuple(point) for point in points}


def test_graph_polylines_explicit_split():
    points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0]]
    graph = line_graph(points)

    polylines = graph_polylines(graph, splits=[points[1]])

    assert normalized_polylines(polylines) == [
        ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
        ((1.0, 0.0, 0.0), (2.0, 0.0, 0.0)),
    ]
