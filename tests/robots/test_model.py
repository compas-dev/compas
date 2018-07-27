import os

import pytest

from compas.robots import Robot

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def urdf_file():
    return os.path.join(BASE_FOLDER, 'fixtures', 'sample.urdf')

def test_root_urdf_attributes():
    r = Robot.from_urdf_string("""<?xml version="1.0" encoding="UTF-8"?><robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="panda"></robot>""")
    assert r.name == 'panda'

def test_unknown_urdf_attributes():
    r = Robot.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot name="panda" some_random_attr="1337"></robot>""")
    assert r.name == 'panda'
    assert r.attr['some_random_attr'] == '1337'

def test_parse_from_file(urdf_file):
    r = Robot.from_urdf_file(urdf_file)
    assert r is not None
    assert r.name == 'panda'

def test_inertial_values(urdf_file):
    r = Robot.from_urdf_file(urdf_file)
    assert r.links[0].inertial.origin is not None
    assert r.links[0].inertial.mass.value == 1.0
    assert r.links[0].inertial.inertia.izz == 100.0
