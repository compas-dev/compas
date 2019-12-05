from math import pi


from compas.geometry import Transformation
from compas.geometry import Translation
from compas.robots import Axis
from compas.robots import Joint
from compas.robots import Limit


def test_revolute_calculate_transformation():
    limit = Limit(lower=-2 * pi, upper=2 * pi)
    j1 = Joint('j1', 'revolute', None, None, limit=limit)
    transformation = j1.calculate_transformation(2*pi)
    assert transformation == Transformation()


def test_prismatic_calculate_transformation():
    limit = Limit(lower=0, upper=1000)
    j1 = Joint('j1', 'prismatic', None, None, axis=Axis('1 0 0'), limit=limit)
    t = j1.calculate_transformation(550)
    assert t == Translation([550, 0, 0])
