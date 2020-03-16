from math import pi


from compas.geometry import Transformation
from compas.geometry import Translation
from compas.robots import Axis
from compas.robots import Joint
from compas.robots import Limit
from compas.robots import Mimic


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


def test_mimic_calculate_transformation():
    multiplier = 5.0
    offset = 100.
    j1 = Joint('j1', 'prismatic', None, None, axis=Axis('1 0 0'))
    j1.position = 200
    mimic = Mimic(j1, multiplier=multiplier, offset=offset)
    result = mimic.calculate_position(j1.position)
    assert result == multiplier * j1.position + offset
