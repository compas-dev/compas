import compas

from compas.geometry import Pointcloud


if not compas.IPY:
    def test_data():
        p = Pointcloud.from_bounds(10, 10, 10, 100)
        assert p.data == p.validate_data()
        o = Pointcloud.from_data(p.data)
        assert p == o
        assert not (p is o)
        assert o.data == o.validate_data()
