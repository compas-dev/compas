from compas.topology import breadth_first_ordering
from compas.topology import breadth_first_paths
from compas.topology import breadth_first_traverse
from compas.topology import breadth_first_tree
from compas.topology import connected_components
from compas.topology import depth_first_ordering
from compas.topology import dijkstra_distances
from compas.topology import dijkstra_path
from compas.topology import edges_from_faces
from compas.topology import faces_from_edges
from compas.topology import shortest_path
from compas.topology import vertex_adjacency_from_edges
from compas.topology import vertex_adjacency_from_faces
from compas.topology import vertex_coloring
from compas.topology.traversal import astar_lightest_path


ADJACENCY = {
    "a": ["b", "c"],
    "b": ["a", "d"],
    "c": ["a", "d"],
    "d": ["b", "c"],
    "isolated": [],
}


def test_connectivity_construction():
    edges = [("a", "b"), ("b", "c"), ("c", "a")]
    faces = [["a", "b", "c"]]

    assert vertex_adjacency_from_edges(iter(edges)) == {
        "a": ["b", "c"],
        "b": ["a", "c"],
        "c": ["b", "a"],
    }
    assert vertex_adjacency_from_faces(faces) == {
        "a": ["b", "c"],
        "b": ["a", "c"],
        "c": ["b", "a"],
    }
    assert edges_from_faces(faces) == edges


def test_faces_from_edges_consumes_input():
    edges = [(0, 1), (1, 2), (2, 0)]
    assert faces_from_edges(edges) == [[2, 0, 1, 2]]
    assert edges == []


def test_combinatorics():
    colors = vertex_coloring(ADJACENCY)
    for node, neighbors in ADJACENCY.items():
        assert all(colors[node] != colors[neighbor] for neighbor in neighbors)

    components = {frozenset(component) for component in connected_components(ADJACENCY)}
    assert components == {frozenset({"a", "b", "c", "d"}), frozenset({"isolated"})}


def test_unweighted_traversal():
    connected = {key: value for key, value in ADJACENCY.items() if key != "isolated"}
    traversed_edges = []

    assert depth_first_ordering(connected, "a")[0] == "a"
    assert set(depth_first_ordering(connected, "a")) == set(connected)
    assert breadth_first_ordering(connected, "a") == ["a", "b", "c", "d"]
    assert breadth_first_traverse(connected, "a", lambda u, v: traversed_edges.append((u, v))) == set(connected)
    assert len(traversed_edges) == len(connected) - 1
    assert {tuple(path) for path in breadth_first_paths(connected, "a", "d")} == {
        ("a", "b", "d"),
        ("a", "c", "d"),
    }
    assert shortest_path(connected, "a", "d") in (["a", "b", "d"], ["a", "c", "d"])
    assert shortest_path(connected, "a", "a") == ["a"]
    assert breadth_first_tree(connected, "a") == (
        ["a", "b", "c", "d"],
        {"b": "a", "c": "a", "d": "b"},
        [["a"], ["a", "b"], ["a", "c"], ["a", "b", "d"]],
    )


def test_weighted_paths_and_identity_paths():
    adjacency = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    weights = {(0, 1): 1.0, (1, 0): 1.0, (0, 2): 5.0, (2, 0): 5.0, (1, 2): 1.0, (2, 1): 1.0}
    heuristic = {0: 2.0, 1: 1.0, 2: 0.0}

    assert dijkstra_distances(adjacency, weights, 2) == {0: 2.0, 1: 1.0, 2: 0}
    assert dijkstra_path(adjacency, weights, 0, 2) == [0, 1, 2]
    assert dijkstra_path(adjacency, weights, 1, 1) == [1]
    assert astar_lightest_path(adjacency, weights, heuristic, 0, 2) == [0, 1, 2]
    assert astar_lightest_path(adjacency, weights, heuristic, 1, 1) == [1]


def test_astar_accepts_non_orderable_hashable_keys_with_equal_priorities():
    first = object()
    second = object()
    goal = object()
    adjacency = {first: [second, goal], second: [first, goal], goal: [first, second]}
    weights = {
        (first, second): 1.0,
        (first, goal): 2.0,
        (second, first): 1.0,
        (second, goal): 1.0,
        (goal, first): 2.0,
        (goal, second): 1.0,
    }
    heuristic = {first: 2.0, second: 1.0, goal: 0.0}

    assert astar_lightest_path(adjacency, weights, heuristic, first, goal) == [first, goal]
