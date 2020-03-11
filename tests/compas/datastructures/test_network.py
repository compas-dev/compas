import pytest

from compas.datastructures import Network
from compas.datastructures import network_is_planar


@pytest.fixture
def k5_network():
    network = Network()
    network.add_edge('a', 'b')
    network.add_edge('a', 'c')
    network.add_edge('a', 'd')
    network.add_edge('a', 'e')

    network.add_edge('b', 'c')
    network.add_edge('b', 'd')
    network.add_edge('b', 'e')

    network.add_edge('c', 'd')
    network.add_edge('c', 'e')

    network.add_edge('d', 'e')

    return network


def test_add_node():
    network = Network()
    assert network.add_node(1) == 1
    assert network.add_node('1', x=0, y=0, z=0) == '1'
    assert network.add_node(2) == 2
    assert network.add_node(0, x=1) == 0


def test_non_planar(k5_network):
    assert network_is_planar(k5_network) is not True


def test_planar(k5_network):
    k5_network.delete_edge('a', 'b')  # Delete (a, b) edge to make K5 planar
    assert network_is_planar(k5_network) is True
