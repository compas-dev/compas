from compas.datastructures import Graph
from compas.datastructures.graph.duality import graph_find_edge_cycle
from compas.datastructures.graph.duality import graph_sort_neighbors
from compas.datastructures.graph.duality import node_sort_neighbors


def square_with_diagonal():
    return Graph.from_lines(
        [
            ([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]),
            ([1.0, 0.0, 0.0], [1.0, 1.0, 0.0]),
            ([1.0, 1.0, 0.0], [0.0, 1.0, 0.0]),
            ([0.0, 1.0, 0.0], [0.0, 0.0, 0.0]),
            ([0.0, 0.0, 0.0], [1.0, 1.0, 0.0]),
        ]
    )


def test_find_cycles_empty_graph():
    assert Graph().find_cycles() == []


def test_find_cycles_edgeless_graph():
    graph = Graph()
    graph.add_node(0, x=0.0, y=0.0, z=0.0)

    assert graph.find_cycles() == []


def test_find_cycles_triangle():
    graph = Graph.from_lines(
        [
            ([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]),
            ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0]),
            ([0.0, 1.0, 0.0], [0.0, 0.0, 0.0]),
        ]
    )

    cycles = graph.find_cycles()

    assert len(cycles) == 1
    assert cycles[0][0] == cycles[0][-1]
    assert set(cycles[0]) == set(graph.nodes())


def test_find_cycles_square_with_diagonal():
    graph = square_with_diagonal()

    cycles = graph.find_cycles()

    assert len(cycles) == 3
    assert sorted(len(cycle) for cycle in cycles) == [4, 4, 5]
    assert all(cycle[0] == cycle[-1] for cycle in cycles)


def test_find_cycles_assigns_cycles_to_adjacency():
    graph = square_with_diagonal()

    graph.find_cycles()

    for u, v in graph.edges():
        assert isinstance(graph.adjacency[u][v], int)
        assert isinstance(graph.adjacency[v][u], int)


def test_find_cycles_with_breakpoints():
    graph = square_with_diagonal()

    cycles = graph.find_cycles(breakpoints=[0, 1])

    assert len(cycles) == 4
    assert [0, 1] in cycles


def test_sort_neighbors():
    graph = Graph.from_lines(
        [
            ([0.0, 0.0, 0.0], [1.0, 0.0, 0.0]),
            ([0.0, 0.0, 0.0], [0.0, 1.0, 0.0]),
            ([0.0, 0.0, 0.0], [-1.0, 0.0, 0.0]),
        ]
    )

    sorted_neighbors = graph_sort_neighbors(graph)

    assert sorted_neighbors[0] == [3, 2, 1]
    assert graph.node_attribute(0, "neighbors") == [1, 2, 3]


def test_sort_neighbors_clockwise():
    xyz = {
        0: [0.0, 0.0, 0.0],
        1: [1.0, 0.0, 0.0],
        2: [0.0, 1.0, 0.0],
        3: [-1.0, 0.0, 0.0],
    }

    ccw = node_sort_neighbors(0, [1, 2, 3], xyz)
    cw = node_sort_neighbors(0, [1, 2, 3], xyz, ccw=False)

    assert cw == ccw[::-1]


def test_find_edge_cycle():
    graph = square_with_diagonal()
    graph_sort_neighbors(graph)

    cycle = graph_find_edge_cycle(graph, (0, 1))

    assert cycle == [0, 1, 2]
