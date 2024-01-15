import json
import os
import random

import pytest

import compas
from compas.datastructures import Network
from compas.geometry import Pointcloud

# ==============================================================================
# Fixtures
# ==============================================================================

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def network():
    edges = [(0, 1), (0, 2), (0, 3), (0, 4)]
    network = Network()
    for u, v in edges:
        network.add_edge(u, v)
    return network


@pytest.fixture
def planar_network():
    return Network.from_obj(os.path.join(BASE_FOLDER, "fixtures", "planar.obj"))


@pytest.fixture
def non_planar_network():
    return Network.from_obj(os.path.join(BASE_FOLDER, "fixtures", "non-planar.obj"))


@pytest.fixture
def k5_network():
    network = Network()
    network.add_edge("a", "b")
    network.add_edge("a", "c")
    network.add_edge("a", "d")
    network.add_edge("a", "e")

    network.add_edge("b", "c")
    network.add_edge("b", "d")
    network.add_edge("b", "e")

    network.add_edge("c", "d")
    network.add_edge("c", "e")

    network.add_edge("d", "e")

    return network


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
def test_network_from_obj(filepath):
    network = Network.from_obj(filepath)
    assert network.number_of_nodes() > 0
    assert network.number_of_edges() > 0
    assert len(list(network.nodes())) == network._max_node + 1
    assert network.is_connected()


def test_network_from_pointcloud():
    cloud = Pointcloud.from_bounds(random.random(), random.random(), random.random(), random.randint(10, 100))
    network = Network.from_pointcloud(cloud=cloud, degree=3)
    assert network.number_of_nodes() == len(cloud)
    for node in network.nodes():
        assert network.degree(node) >= 3


# ==============================================================================
# Data
# ==============================================================================


def test_network_data1(network):
    other = Network.from_data(json.loads(json.dumps(network.data)))

    assert network.data == other.data
    assert network.default_node_attributes == other.default_node_attributes
    assert network.default_edge_attributes == other.default_edge_attributes
    assert network.number_of_nodes() == other.number_of_nodes()
    assert network.number_of_edges() == other.number_of_edges()

    if not compas.IPY:
        assert Network.validate_data(network.data)
        assert Network.validate_data(other.data)


def test_network_data2():
    cloud = Pointcloud.from_bounds(random.random(), random.random(), random.random(), random.randint(10, 100))
    network = Network.from_pointcloud(cloud=cloud, degree=3)
    other = Network.from_data(json.loads(json.dumps(network.data)))

    assert network.data == other.data

    if not compas.IPY:
        assert Network.validate_data(network.data)
        assert Network.validate_data(other.data)


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
    network = Network()
    assert network.add_node(1) == 1
    assert network.add_node("1", x=0, y=0, z=0) == "1"
    assert network.add_node(2) == 2
    assert network.add_node(0, x=1) == 0


# ==============================================================================
# Modifiers
# ==============================================================================


def test_network_invalid_edge_delete():
    network = Network()
    node = network.add_node()
    edge = network.add_edge(node, node)
    network.delete_edge(edge)
    assert network.has_edge(edge) is False


def test_network_opposite_direction_edge_delete():
    network = Network()
    node_a = network.add_node()
    node_b = network.add_node()
    edge_a = network.add_edge(node_a, node_b)
    edge_b = network.add_edge(node_b, node_a)
    network.delete_edge(edge_a)
    assert network.has_edge(edge_a) is False
    assert network.has_edge(edge_b) is True


# ==============================================================================
# Samples
# ==============================================================================


def test_network_node_sample(network):
    for node in network.node_sample():
        assert network.has_node(node)
    for node in network.node_sample(size=network.number_of_nodes()):
        assert network.has_node(node)


def test_network_edge_sample(network):
    for edge in network.edge_sample():
        assert network.has_edge(edge)
    for edge in network.edge_sample(size=network.number_of_edges()):
        assert network.has_edge(edge)


# ==============================================================================
# Attributes
# ==============================================================================


def test_network_default_node_attributes():
    network = Network(name="test", default_node_attributes={"a": 1, "b": 2})
    for node in network.nodes():
        assert network.node_attribute(node, name="a") == 1
        assert network.node_attribute(node, name="b") == 2
        network.node_attribute(node, name="a", value=3)
        assert network.node_attribute(node, name="a") == 3


def test_network_default_edge_attributes():
    network = Network(name="test", default_edge_attributes={"a": 1, "b": 2})
    for edge in network.edges():
        assert network.edge_attribute(edge, name="a") == 1
        assert network.edge_attribute(edge, name="b") == 2
        network.edge_attribute(edge, name="a", value=3)
        assert network.edge_attribute(edge, name="a") == 3


# ==============================================================================
# Conversion
# ==============================================================================


def test_network_to_networkx():
    if compas.IPY:
        return

    g = Network()
    g.attributes["name"] = "DiGraph"
    g.attributes["val"] = (0, 0, 0)
    g.add_node(0)
    g.add_node(1, weight=1.2, height="test")
    g.add_node(2, x=1, y=1, z=0)

    g.add_edge(0, 1, attr_value=10)
    g.add_edge(1, 2)

    nxg = g.to_networkx()

    assert nxg.graph["name"] == "DiGraph", "Network attributes must be preserved"  # type: ignore
    assert nxg.graph["val"] == (0, 0, 0), "Network attributes must be preserved"  # type: ignore
    assert set(nxg.nodes()) == set(g.nodes()), "Node sets must match"
    assert nxg.nodes[1]["weight"] == 1.2, "Node attributes must be preserved"
    assert nxg.nodes[1]["height"] == "test", "Node attributes must be preserved"
    assert nxg.nodes[2]["x"] == 1, "Node attributes must be preserved"

    assert set(nxg.edges()) == set(((0, 1), (1, 2))), "Edge sets must match"
    assert nxg.edges[0, 1]["attr_value"] == 10, "Edge attributes must be preserved"

    g2 = Network.from_networkx(nxg)

    assert g.number_of_nodes() == g2.number_of_nodes()
    assert g.number_of_edges() == g2.number_of_edges()
    assert g2.edge_attribute((0, 1), "attr_value") == 10
    assert g2.attributes["name"] == "DiGraph", "Network attributes must be preserved"
    assert g2.attributes["val"] == (0, 0, 0), "Network attributes must be preserved"


# ==============================================================================
# Methods
# ==============================================================================


def test_non_planar(k5_network, non_planar_network):
    if not compas.IPY:
        assert k5_network.is_planar() is not True
        assert non_planar_network.is_planar() is not True


def test_planar(k5_network, planar_network):
    if not compas.IPY:
        k5_network.delete_edge(("a", "b"))  # Delete (a, b) edge to make K5 planar
        assert k5_network.is_planar() is True
        assert planar_network.is_planar() is True
