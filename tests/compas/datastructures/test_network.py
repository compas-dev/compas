import pytest
import compas
import json
from random import random, randint

from compas.datastructures import Network
from compas.geometry import Pointcloud


# ==============================================================================
# Fixtures
# ==============================================================================


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
    cloud = Pointcloud.from_bounds(random(), random(), random(), randint(10, 100))
    network = Network.from_pointcloud(cloud=cloud, degree=3)
    assert network.number_of_nodes() == len(cloud)
    for node in network.nodes():
        assert network.degree(node) >= 3


# ==============================================================================
# Data
# ==============================================================================


def test_network_data():
    cloud = Pointcloud.from_bounds(random(), random(), random(), randint(10, 100))
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

# ==============================================================================
# Samples
# ==============================================================================

# ==============================================================================
# Attributes
# ==============================================================================

# ==============================================================================
# Conversion
# ==============================================================================

# ==============================================================================
# Methods
# ==============================================================================


def test_non_planar(k5_network):
    try:
        import planarity  # noqa: F401
    except ImportError:
        return

    from compas.datastructures import network_is_planar

    assert network_is_planar(k5_network) is not True


def test_planar(k5_network):
    try:
        import planarity  # noqa: F401
    except ImportError:
        return

    from compas.datastructures import network_is_planar

    k5_network.delete_edge(("a", "b"))  # Delete (a, b) edge to make K5 planar
    assert network_is_planar(k5_network) is True
