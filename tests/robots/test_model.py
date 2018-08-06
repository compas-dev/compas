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


@pytest.fixture
def ur5_file():
    return os.path.join(BASE_FOLDER, 'fixtures', 'ur5.xacro')


def test_ur5_urdf(ur5_file):
    r = Robot.from_urdf_file(ur5_file)
    assert r.name == 'ur5'
    assert len(list(filter(lambda i: i.type == 'revolute', r.joints))) == 6


def test_root_urdf_attributes():
    r = Robot.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="panda"></robot>""")
    assert r.name == 'panda'


def test_robot_material_attributes():
    r = Robot.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot name="panda"><material name="LightGrey"><color rgba="0.7 0.7 0.7 1.0"/></material></robot>""")
    assert r.materials[0].color.rgba == [0.7, 0.7, 0.7, 1.0]


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
    assert r.links[0].visual[0].geometry.shape.scale == [1.0, 1.0, 1.0]

    assert type(r.links[0].collision[0].geometry.shape) == Sphere
    assert r.links[0].collision[0].geometry.shape.radius == 200.

    assert type(r.links[1].visual[0].geometry.shape) == Box
    assert r.links[1].visual[0].geometry.shape.size == [600., 100., 200.]

    assert type(r.links[1].collision[0].geometry.shape) == Cylinder
    assert r.links[1].collision[0].geometry.shape.length == 600.
    assert r.links[1].collision[0].geometry.shape.radius == 200.


if __name__ == '__main__':
    import os
    from zipfile import ZipFile
    try:
        from StringIO import StringIO as ReaderIO
        from urllib import urlopen
    except ImportError:
        from io import BytesIO as ReaderIO
        from urllib.request import urlopen

    print('Downloading large collection of URDF from Drake project...')
    print('This might take a few minutes...')
    resp = urlopen('https://github.com/RobotLocomotion/drake/archive/master.zip')
    zipfile = ZipFile(ReaderIO(resp.read()))
    errors = []
    all_files = []

    for f in zipfile.namelist():
        if f.endswith('.urdf') or f.endswith('.xacro'):
            with zipfile.open(f) as urdf_file:
                try:
                    all_files.append(f)
                    r = Robot.from_urdf_file(urdf_file)
                except Exception as e:
                    errors.append((f, e))

    print('Found %d files and parsed successfully %d of them' %
          (len(all_files), len(all_files) - len(errors)))

    if len(errors):
        print('\nErrors found during parsing:')
        for error in errors:
            print(' * File=%s, Error=%s' % error)
