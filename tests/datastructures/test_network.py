from compas.datastructures import Network


def test_add_vertex():
    network = Network()
    assert network.add_vertex() == 0
    assert network.add_vertex(x=0, y=0, z=0) == 1
    assert network.add_vertex(key=2) == 2
    assert network.add_vertex(key=0, x=1) == 0
