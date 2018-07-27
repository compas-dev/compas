import os

import pytest

from compas.robots import Robot, Box, Cylinder, Sphere

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def urdf_file():
    return os.path.join(BASE_FOLDER, 'fixtures', 'sample.urdf')


@pytest.fixture
def urdf_file_with_shapes():
    return os.path.join(BASE_FOLDER, 'fixtures', 'sample.with_shapes.urdf')

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

def test_inertial_parser(urdf_file):
    r = Robot.from_urdf_file(urdf_file)
    assert r.links[0].inertial.origin is not None
    assert r.links[0].inertial.origin.point == [0.0, 0.0, 0.0]
    assert r.links[0].inertial.mass.value == 1.0
    assert r.links[0].inertial.inertia.izz == 100.0

def test_link_parser(urdf_file):
    r = Robot.from_urdf_file(urdf_file)

    assert r.links[0].name == 'panda_link0'
    assert r.links[1].name == 'panda_link1'
    assert r.links[2].name == 'panda_link2'

    assert r.links[0].type == 'test_type'

    assert len(r.links) == 12


def test_geometry_parser(urdf_file_with_shapes):
    r = Robot.from_urdf_file(urdf_file_with_shapes)

    assert r.links[0].visual[0].geometry.shape.filename == 'package://franka_description/meshes/visual/link0.dae'
    assert r.links[0].visual[0].geometry.shape.scale == 1.


    assert type(r.links[0].collision[0].geometry.shape) == Sphere
    assert r.links[0].collision[0].geometry.shape.radius == 200.

    assert type(r.links[1].visual[0].geometry.shape) == Box
    assert r.links[1].visual[0].geometry.shape.size == [600., 100., 200.]

    assert type(r.links[1].collision[0].geometry.shape) == Cylinder
    assert r.links[1].collision[0].geometry.shape.length == 600.
    assert r.links[1].collision[0].geometry.shape.radius == 200.
