import compas

from compas.datastructures import Network
from compas.datastructures import network_is_planar


def test_add_vertex():
    network = Network()
    assert network.add_vertex() == 0
    assert network.add_vertex(x=0, y=0, z=0) == 1
    assert network.add_vertex(key=2) == 2
    assert network.add_vertex(key=0, x=1) == 0

def test_planarity():
    network = Network.from_obj(compas.get('lines.obj'))
    network.add_edge(6, 15)
    assert network_is_planar(network) is not True
