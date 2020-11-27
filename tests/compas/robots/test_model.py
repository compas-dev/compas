import os

import pytest

from compas.files import URDF
from compas.robots import Box
from compas.robots import Cylinder
from compas.robots import Joint
from compas.robots import Link
from compas.robots import RobotModel
from compas.robots import Sphere

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


@pytest.fixture
def urdf_with_unknown_attr():
    return os.path.join(BASE_FOLDER, 'fixtures', 'sample_unknown_attributes.urdf')


@pytest.fixture
def ur5():
    """Return a UR5 created programmatically instead of from a file."""
    return RobotModel('ur5',
                      joints=[
                          Joint('shoulder_pan_joint', 'revolute', 'base_link', 'shoulder_link'),
                          Joint('shoulder_lift_joint', 'revolute', 'shoulder_link', 'upper_arm_link'),
                          Joint('elbow_joint', 'revolute', 'upper_arm_link', 'forearm_link'),
                          Joint('wrist_1_joint', 'revolute', 'forearm_link', 'wrist_1_link'),
                          Joint('wrist_2_joint', 'revolute', 'wrist_1_link', 'wrist_2_link'),
                          Joint('wrist_3_joint', 'revolute', 'wrist_2_link', 'wrist_3_link'),
                      ], links=[
                          Link('base_link'),
                          Link('shoulder_link'),
                          Link('upper_arm_link'),
                          Link('forearm_link'),
                          Link('wrist_1_link'),
                          Link('wrist_2_link'),
                          Link('wrist_3_link'),
                      ]
                      )


def test_programmatic_robot_model():
    robot = RobotModel("robot")
    link0 = robot.add_link("link0")
    link1 = robot.add_link("link1")
    robot.add_joint("joint1", Joint.CONTINUOUS, link0, link1)
    assert(['link0', 'joint1', 'link1'] == list(robot.iter_chain()))
    link2 = robot.add_link("link2")
    robot.add_joint("joint2", Joint.CONTINUOUS, link1, link2)
    assert(['link0', 'joint1', 'link1', 'joint2', 'link2'] == list(robot.iter_chain()))
    urdf = URDF.from_robot(robot)
    robot_reincarnated = RobotModel.from_urdf_string(urdf.to_string())
    assert(['link0', 'joint1', 'link1', 'joint2', 'link2'] == list(robot_reincarnated.iter_chain()))


def test_ur5_urdf(ur5_file):
    r = RobotModel.from_urdf_file(ur5_file)
    assert r.name == 'ur5'
    assert len(list(filter(lambda i: i.type == Joint.REVOLUTE, r.joints))) == 6


def test_ur5_urdf_to_string(ur5_file):
    r_original = RobotModel.from_urdf_file(ur5_file)
    urdf = URDF.from_robot(r_original)
    r = RobotModel.from_urdf_string(urdf.to_string())
    assert r.name == 'ur5'
    assert len(list(filter(lambda i: i.type == Joint.REVOLUTE, r.joints))) == 6


def test_ur5_urdf_data(ur5_file):
    r_original = RobotModel.from_urdf_file(ur5_file)
    r = RobotModel.from_data(r_original.data)
    assert r.name == 'ur5'
    assert len(list(filter(lambda i: i.type == Joint.REVOLUTE, r.joints))) == 6


def test_root_urdf_attributes():
    r = RobotModel.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="panda"></robot>""")
    assert r.name == 'panda'


def test_root_urdf_attributes_to_string():
    r = RobotModel.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="panda"></robot>""")
    urdf_string = URDF.from_robot(r).to_string(prettify=True)
    assert b'name="panda"' in urdf_string


def test_robot_urdf_namespaces_to_string():
    r = RobotModel.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="panda"><xacro:bamboo/></robot>""")
    urdf_string = URDF.from_robot(r).to_string(prettify=True)
    assert b'xmlns:xacro="http://www.ros.org/wiki/xacro"' in urdf_string
    assert b'<xacro:bamboo' in urdf_string or b'<ns0:bamboo'
    # Note: Minidom does some funny things to namespaces.  First, if a namespace isn't used, it will be stripped out.
    # Second, it will include the original namespace declaration, but also repeat that declaration with another name,
    # and replace all references to the original with the new.


def test_programmatic_model(ur5):
    chain = list(ur5.iter_chain('base_link', 'wrist_3_link'))
    expected_chain = [
        'base_link',
        'shoulder_pan_joint',
        'shoulder_link',
        'shoulder_lift_joint',
        'upper_arm_link',
        'elbow_joint',
        'forearm_link',
        'wrist_1_joint',
        'wrist_1_link',
        'wrist_2_joint',
        'wrist_2_link',
        'wrist_3_joint',
        'wrist_3_link'
    ]

    assert ur5.name == 'ur5'
    assert chain == expected_chain

    urdf = URDF.from_robot(ur5)
    ur5_reincarnated = RobotModel.from_urdf_string(urdf.to_string())
    chain = list(ur5_reincarnated.iter_chain('base_link', 'wrist_3_link'))

    assert ur5_reincarnated.name == 'ur5'
    assert chain == expected_chain


def test_robot_material_attributes():
    r = RobotModel.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot name="panda"><material name="LightGrey"><color rgba="0.7 0.7 0.7 1.0"/></material></robot>""")
    assert r.materials[0].color.rgba == [0.7, 0.7, 0.7, 1.0]


def test_robot_material_attributes_to_string():
    r_original = RobotModel.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot name="panda"><material name="LightGrey"><color rgba="0.7 0.7 0.7 1.0"/></material></robot>""")
    urdf = URDF.from_robot(r_original)
    r = RobotModel.from_urdf_string(urdf.to_string())
    assert r.materials[0].color.rgba == [0.7, 0.7, 0.7, 1.0]


def test_unknown_urdf_attributes():
    r = RobotModel.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot name="panda" some_random_attr="1337"></robot>""")
    assert r.name == 'panda'
    assert r.attr['some_random_attr'] == '1337'


def test_unknown_urdf_attributes_to_string():
    r_original = RobotModel.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot name="panda" some_random_attr="1337"></robot>""")
    urdf = URDF.from_robot(r_original)
    r = RobotModel.from_urdf_string(urdf.to_string())
    assert r.attr['some_random_attr'] == '1337'


def test_unknown_urdf_attributes_data():
    r_original = RobotModel.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot name="panda" some_random_attr="1337"></robot>""")
    r = RobotModel.from_data(r_original.data)
    assert r.name == 'panda'
    assert r.attr['some_random_attr'] == '1337'


def test_parse_from_file(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    assert r is not None
    assert r.name == 'panda'


def test_parse_from_file_data(urdf_file):
    r_original = RobotModel.from_urdf_file(urdf_file)
    r = RobotModel.from_data(r_original.data)
    assert r is not None
    assert r.name == 'panda'


def test_inertial_parser(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    assert r.links[0].inertial.origin is not None
    assert r.links[0].inertial.origin.point == [0.0, 0.0, 0.5]
    assert r.links[0].inertial.mass.value == 1.0
    assert r.links[0].inertial.inertia.izz == 100.0


def test_inertial_parser_to_string(urdf_file):
    r_original = RobotModel.from_urdf_file(urdf_file)
    urdf = URDF.from_robot(r_original)
    r = RobotModel.from_urdf_string(urdf.to_string())
    assert r.links[0].inertial.origin is not None
    assert r.links[0].inertial.origin.point == [0.0, 0.0, 0.5]
    assert r.links[0].inertial.mass.value == 1.0
    assert r.links[0].inertial.inertia.izz == 100.0


def test_inertial_parser_data(urdf_file):
    r_original = RobotModel.from_urdf_file(urdf_file)
    r = RobotModel.from_data(r_original.data)
    assert r.links[0].inertial.origin is not None
    assert r.links[0].inertial.origin.point == [0.0, 0.0, 0.5]
    assert r.links[0].inertial.mass.value == 1.0
    assert r.links[0].inertial.inertia.izz == 100.0


def test_link_parser(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)

    assert r.links[0].name == 'panda_link0'
    assert r.links[1].name == 'panda_link1'
    assert r.links[2].name == 'panda_link2'

    assert r.links[0].type == 'test_type'

    assert len(r.links) == 12


def test_link_parser_to_string(urdf_file):
    r_original = RobotModel.from_urdf_file(urdf_file)
    urdf = URDF.from_robot(r_original)
    r = RobotModel.from_urdf_string(urdf.to_string())

    assert r.links[0].name == 'panda_link0'
    assert r.links[1].name == 'panda_link1'
    assert r.links[2].name == 'panda_link2'

    assert r.links[0].type == 'test_type'

    assert len(r.links) == 12


def test_link_parser_data(urdf_file):
    r_original = RobotModel.from_urdf_file(urdf_file)
    r = RobotModel.from_data(r_original.data)

    assert r.links[0].name == 'panda_link0'
    assert r.links[1].name == 'panda_link1'
    assert r.links[2].name == 'panda_link2'

    assert r.links[0].type == 'test_type'

    assert len(r.links) == 12


def test_geometry_parser(urdf_file_with_shapes):
    r = RobotModel.from_urdf_file(urdf_file_with_shapes)

    assert r.links[0].visual[0].geometry.shape.filename == 'package://franka_description/meshes/visual/link0.dae'
    assert r.links[0].visual[0].geometry.shape.scale == [1.0, 1.0, 1.0]

    assert type(r.links[0].collision[0].geometry.shape) == Sphere
    assert r.links[0].collision[0].geometry.shape.radius == 0.2

    assert type(r.links[1].visual[0].geometry.shape) == Box
    assert r.links[1].visual[0].geometry.shape.size == [0.6, 0.1, 0.2]

    assert type(r.links[1].collision[0].geometry.shape) == Cylinder
    assert r.links[1].collision[0].geometry.shape.length == 0.6
    assert r.links[1].collision[0].geometry.shape.radius == 0.2


def test_geometry_parser_to_string(urdf_file_with_shapes):
    r_original = RobotModel.from_urdf_file(urdf_file_with_shapes)
    urdf = URDF.from_robot(r_original)
    r = RobotModel.from_urdf_string(urdf.to_string())

    assert r.links[0].visual[0].geometry.shape.filename == 'package://franka_description/meshes/visual/link0.dae'
    assert r.links[0].visual[0].geometry.shape.scale == [1.0, 1.0, 1.0]

    assert type(r.links[0].collision[0].geometry.shape) == Sphere
    assert r.links[0].collision[0].geometry.shape.radius == 0.2

    assert type(r.links[1].visual[0].geometry.shape) == Box
    assert r.links[1].visual[0].geometry.shape.size == [0.6, 0.1, 0.2]

    assert type(r.links[1].collision[0].geometry.shape) == Cylinder
    assert r.links[1].collision[0].geometry.shape.length == 0.6
    assert r.links[1].collision[0].geometry.shape.radius == 0.2


def test_geometry_parser_data(urdf_file_with_shapes):
    r_original = RobotModel.from_urdf_file(urdf_file_with_shapes)
    r = RobotModel.from_data(r_original.data)

    assert r.links[0].visual[0].geometry.shape.filename == 'package://franka_description/meshes/visual/link0.dae'
    assert r.links[0].visual[0].geometry.shape.scale == [1.0, 1.0, 1.0]

    assert type(r.links[0].collision[0].geometry.shape) == Sphere
    assert r.links[0].collision[0].geometry.shape.radius == 0.2

    assert type(r.links[1].visual[0].geometry.shape) == Box
    assert r.links[1].visual[0].geometry.shape.size == [0.6, 0.1, 0.2]

    assert type(r.links[1].collision[0].geometry.shape) == Cylinder
    assert r.links[1].collision[0].geometry.shape.length == 0.6
    assert r.links[1].collision[0].geometry.shape.radius == 0.2


def test_root(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    assert 'panda_link0' == r.root.name


def test_root_data(urdf_file):
    r_original = RobotModel.from_urdf_file(urdf_file)
    r = RobotModel.from_data(r_original.data)
    assert 'panda_link0' == r.root.name


def test_root_getter_without_links():
    r = RobotModel.from_urdf_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot name="panda"></robot>""")
    assert r.root is None


def test_get_link_by_name(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    hand = r.get_link_by_name('panda_hand')
    assert hand is not None

    invalid_link_name = r.get_link_by_name('nonexistent')
    assert invalid_link_name is None


def test_get_joint_by_name(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    finger_joint = r.get_joint_by_name('panda_finger_joint1')
    assert finger_joint is not None

    invalid_joint_name = r.get_joint_by_name('nonexistent')
    assert invalid_joint_name is None


def test_get_end_effector_link(ur5_file):
    r = RobotModel.from_urdf_file(ur5_file)
    assert r.get_end_effector_link().name == 'ee_link'


def test_get_end_effector_link_name(ur5_file):
    r = RobotModel.from_urdf_file(ur5_file)
    assert r.get_end_effector_link_name() == 'ee_link'


def test_find_children_joints(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    link1 = r.get_link_by_name('panda_link1')
    joints = r.find_children_joints(link1)
    assert len(joints) == 1
    assert joints[0].name == 'panda_joint2'

    hand = r.get_link_by_name('panda_hand')
    joints = r.find_children_joints(hand)
    assert len(joints) == 2
    assert joints[0].name == 'panda_finger_joint1'
    assert joints[1].name == 'panda_finger_joint2'

    finger = r.get_link_by_name('panda_rightfinger')
    joints = r.find_children_joints(finger)
    assert len(joints) == 0


def test_child_link(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    assert r.joints[0].name == 'panda_joint1'   # Check assumption before test

    assert r.joints[0].child_link.name == 'panda_link1'


def test_find_parent_joint(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    root_link = r.root
    assert r.find_parent_joint(root_link) is None

    link4 = r.get_link_by_name('panda_link4')
    joint = r.find_parent_joint(link4)
    assert joint.name == 'panda_joint4'


def test_iter_links(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    links = [link.name for link in r.iter_links()]
    expected_links = [
        'panda_link0',
        'panda_link1',
        'panda_link2',
        'panda_link3',
        'panda_link4',
        'panda_link5',
        'panda_link6',
        'panda_link7',
        'panda_link8',
        'panda_hand',
        'panda_leftfinger',
        'panda_rightfinger',
    ]
    assert links == expected_links


def test_iter_joints(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    joints = [joint.name for joint in r.iter_joints()]
    expected_joints = [
        'panda_joint1',
        'panda_joint2',
        'panda_joint3',
        'panda_joint4',
        'panda_joint5',
        'panda_joint6',
        'panda_joint7',
        'panda_joint8',
        'panda_hand_joint',
        'panda_finger_joint1',
        'panda_finger_joint2',
    ]
    assert joints == expected_joints


def test_iter_link_chain(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    names = [i.name for i in r.iter_link_chain(
        'panda_link2', 'panda_rightfinger')]
    expected_chain = [
        'panda_link2',
        'panda_link3',
        'panda_link4',
        'panda_link5',
        'panda_link6',
        'panda_link7',
        'panda_link8',
        'panda_hand',
        'panda_rightfinger',
    ]
    assert names == expected_chain


def test_iter_link_chain_defaults(urdf_file):
    r = RobotModel.from_urdf_file(urdf_file)
    names = [i.name for i in r.iter_link_chain()]
    expected_chain = [
        'panda_link0',
        'panda_link1',
        'panda_link2',
        'panda_link3',
        'panda_link4',
        'panda_link5',
        'panda_link6',
        'panda_link7',
        'panda_link8',
        'panda_hand',
        'panda_rightfinger',
    ]
    assert names == expected_chain


def test_unknown_axis_attribute(urdf_with_unknown_attr):
    r = RobotModel.from_urdf_file(urdf_with_unknown_attr)
    assert r.joints[0].axis.attr['rpy'] == '0 0 0'


def test_unknown_axis_attribute_to_string(urdf_with_unknown_attr):
    r_original = RobotModel.from_urdf_file(urdf_with_unknown_attr)
    urdf = URDF.from_robot(r_original)
    urdf_string = urdf.to_string().decode('utf-8')
    r = RobotModel.from_urdf_string(urdf_string)
    assert r.joints[0].axis.attr['rpy'] == '0 0 0'
    assert """<random name="random_tag">""" in urdf_string
    assert """<random_other>TEXT</random_other>""" in urdf_string


def test_unknown_axis_attribute_data(urdf_with_unknown_attr):
    r_original = RobotModel.from_urdf_file(urdf_with_unknown_attr)
    r = RobotModel.from_data(r_original.data)
    assert r.joints[0].axis.attr['rpy'] == '0 0 0'


# ==============================================================================
# Main
# ==============================================================================

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
            with zipfile.open(f) as urdffile:
                try:
                    all_files.append(f)
                    r = RobotModel.from_urdf_file(urdffile)
                    urdf = URDF.from_robot(r)
                    r2 = RobotModel.from_urdf_string(urdf.to_string())
                except Exception as e:
                    errors.append((f, e))

    print('Found %d files and parsed successfully %d of them' %
          (len(all_files), len(all_files) - len(errors)))

    if len(errors):
        print('\nErrors found during parsing:')
        for error in errors:
            print(' * File=%s, Error=%s' % error)
