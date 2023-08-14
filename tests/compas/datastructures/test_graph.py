import pytest
import json
import compas

from compas.datastructures import Graph


# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def graph():
    edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
    graph = Graph()
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


# ==============================================================================
# Basics
# ==============================================================================

# ==============================================================================
# Data
# ==============================================================================


def test_graph_data(graph):
    other = Graph.from_data(json.loads(json.dumps(graph.data)))

    assert graph.data == other.data
    assert graph.default_node_attributes == other.default_node_attributes
    assert graph.default_edge_attributes == other.default_edge_attributes
    assert graph.number_of_nodes() == other.number_of_nodes()
    assert graph.number_of_edges() == other.number_of_edges()

    if not compas.IPY:
        assert Graph.validate_data(graph.data)
        assert Graph.validate_data(other.data)


# ==============================================================================
# Constructors
# ==============================================================================

# ==============================================================================
# Properties
# ==============================================================================

# ==============================================================================
# Accessors
# ==============================================================================

# ==============================================================================
# Builders
# ==============================================================================

# ==============================================================================
# Modifiers
# ==============================================================================


def test_graph_invalid_edge_delete():
    graph = Graph()
    node = graph.add_node()
    edge = graph.add_edge(node, node)
    graph.delete_edge(edge)
    assert graph.has_edge(edge) is False


def test_graph_opposite_direction_edge_delete():
    graph = Graph()
    node_a = graph.add_node()
    node_b = graph.add_node()
    edge_a = graph.add_edge(node_a, node_b)
    edge_b = graph.add_edge(node_b, node_a)
    graph.delete_edge(edge_a)
    assert graph.has_edge(edge_a) is False
    assert graph.has_edge(edge_b) is True


# ==============================================================================
# Samples
# ==============================================================================


def test_graph_node_sample(graph):
    for node in graph.node_sample():
        assert graph.has_node(node)
    for node in graph.node_sample(size=graph.number_of_nodes()):
        assert graph.has_node(node)


def test_graph_edge_sample(graph):
    for edge in graph.edge_sample():
        assert graph.has_edge(edge)
    for edge in graph.edge_sample(size=graph.number_of_edges()):
        assert graph.has_edge(edge)


# ==============================================================================
# Attributes
# ==============================================================================


def test_graph_default_node_attributes():
    graph = Graph(name="test", default_node_attributes={"a": 1, "b": 2})
    for node in graph.nodes():
        assert graph.node_attribute(node, name="a") == 1
        assert graph.node_attribute(node, name="b") == 2
        graph.node_attribute(node, name="a", value=3)
        assert graph.node_attribute(node, name="a") == 3


def test_graph_default_edge_attributes():
    graph = Graph(name="test", default_edge_attributes={"a": 1, "b": 2})
    for edge in graph.edges():
        assert graph.edge_attribute(edge, name="a") == 1
        assert graph.edge_attribute(edge, name="b") == 2
        graph.edge_attribute(edge, name="a", value=3)
        assert graph.edge_attribute(edge, name="a") == 3


# ==============================================================================
# Conversion
# ==============================================================================


def test_graph_to_networkx():
    if compas.IPY:
        return

    g = Graph()
    g.attributes["name"] = "DiGraph"
    g.attributes["val"] = (0, 0, 0)
    g.add_node(0)
    g.add_node(1, weight=1.2, height="test")
    g.add_node(2, x=1, y=1, z=0)

    g.add_edge(0, 1, attr_value=10)
    g.add_edge(1, 2)

    nxg = g.to_networkx()

    assert nxg.graph["name"] == "DiGraph", "Graph attributes must be preserved"  # type: ignore
    assert nxg.graph["val"] == (0, 0, 0), "Graph attributes must be preserved"  # type: ignore
    assert set(nxg.nodes()) == set(g.nodes()), "Node sets must match"
    assert nxg.nodes[1]["weight"] == 1.2, "Node attributes must be preserved"
    assert nxg.nodes[1]["height"] == "test", "Node attributes must be preserved"
    assert nxg.nodes[2]["x"] == 1, "Node attributes must be preserved"

    assert set(nxg.edges()) == set(((0, 1), (1, 2))), "Edge sets must match"
    assert nxg.edges[0, 1]["attr_value"] == 10, "Edge attributes must be preserved"

    g2 = Graph.from_networkx(nxg)

    assert g.number_of_nodes() == g2.number_of_nodes()
    assert g.number_of_edges() == g2.number_of_edges()
    assert g2.edge_attribute((0, 1), "attr_value") == 10
    assert g2.attributes["name"] == "DiGraph", "Graph attributes must be preserved"
    assert g2.attributes["val"] == (0, 0, 0), "Graph attributes must be preserved"
