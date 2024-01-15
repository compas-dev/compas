import json
import os
import random

import pytest

import compas
from compas.datastructures import Graph
from compas.geometry import Pointcloud

# ==============================================================================
# Fixtures
# ==============================================================================

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def graph():
    edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
    graph = Graph()
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


@pytest.fixture
def planar_graph():
    return Graph.from_obj(os.path.join(BASE_FOLDER, "fixtures", "planar.obj"))


@pytest.fixture
def non_planar_graph():
    return Graph.from_obj(os.path.join(BASE_FOLDER, "fixtures", "non-planar.obj"))


@pytest.fixture
def k5_graph():
    graph = Graph()
    graph.add_edge("a", "b")
    graph.add_edge("a", "c")
    graph.add_edge("a", "d")
    graph.add_edge("a", "e")

    graph.add_edge("b", "c")
    graph.add_edge("b", "d")
    graph.add_edge("b", "e")

    graph.add_edge("c", "d")
    graph.add_edge("c", "e")

    graph.add_edge("d", "e")

    return graph


# ==============================================================================
# Basics
# ==============================================================================

# ==============================================================================
# Constructors
# ==============================================================================


@pytest.mark.parametrize(
    "filepath",
    [
        compas.get("lines.obj"),
        compas.get("grid_irregular.obj"),
    ],
)
def test_graph_from_obj(filepath):
    graph = Graph.from_obj(filepath)
    assert graph.number_of_nodes() > 0
    assert graph.number_of_edges() > 0
    assert len(list(graph.nodes())) == graph._max_node + 1
    assert graph.is_connected()


def test_graph_from_pointcloud():
    cloud = Pointcloud.from_bounds(random.random(), random.random(), random.random(), random.randint(10, 100))
    graph = Graph.from_pointcloud(cloud=cloud, degree=3)
    assert graph.number_of_nodes() == len(cloud)
    for node in graph.nodes():
        assert graph.degree(node) >= 3


# ==============================================================================
# Data
# ==============================================================================


def test_graph_data1(graph):
    other = Graph.from_data(json.loads(json.dumps(graph.data)))

    assert graph.data == other.data
    assert graph.default_node_attributes == other.default_node_attributes
    assert graph.default_edge_attributes == other.default_edge_attributes
    assert graph.number_of_nodes() == other.number_of_nodes()
    assert graph.number_of_edges() == other.number_of_edges()

    if not compas.IPY:
        assert Graph.validate_data(graph.data)
        assert Graph.validate_data(other.data)


def test_graph_data2():
    cloud = Pointcloud.from_bounds(random.random(), random.random(), random.random(), random.randint(10, 100))
    graph = Graph.from_pointcloud(cloud=cloud, degree=3)
    other = Graph.from_data(json.loads(json.dumps(graph.data)))

    assert graph.data == other.data

    if not compas.IPY:
        assert Graph.validate_data(graph.data)
        assert Graph.validate_data(other.data)


# ==============================================================================
# Properties
# ==============================================================================

# ==============================================================================
# Accessors
# ==============================================================================

# ==============================================================================
# Builders
# ==============================================================================


def test_add_node():
    graph = Graph()
    assert graph.add_node(1) == 1
    assert graph.add_node("1", x=0, y=0, z=0) == "1"
    assert graph.add_node(2) == 2
    assert graph.add_node(0, x=1) == 0


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


def test_network_to_networkx():
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


# ==============================================================================
# Methods
# ==============================================================================


def test_non_planar(k5_graph, non_planar_graph):
    if not compas.IPY:
        assert k5_graph.is_planar() is not True
        assert non_planar_graph.is_planar() is not True


def test_planar(k5_graph, planar_graph):
    if not compas.IPY:
        k5_graph.delete_edge(("a", "b"))  # Delete (a, b) edge to make K5 planar
        assert k5_graph.is_planar() is True
        assert planar_graph.is_planar() is True
