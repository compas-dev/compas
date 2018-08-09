from __future__ import absolute_import, division, print_function

from compas.files import URDF
from compas.geometry import Frame

# URDF is defined in meters
# so we scale it all to millimeters
SCALE_FACTOR = 1000

__all__ = ['Robot', 'Joint', 'Link', 'Inertial', 'Visual', 'Collision',
           'Geometry', 'Box', 'Cylinder', 'Sphere', 'Capsule', 'MeshDescriptor',
           'Color', 'Texture', 'Material', 'Origin', 'Mass', 'Inertia',
           'ParentJoint', 'ChildJoint', 'Calibration', 'Dynamics', 'Limit',
           'Axis', 'Mimic', 'SafetyController']


def _parse_floats(values, scale_factor=None):
    result = []

    for i in values.split():
        val = float(i)
        if scale_factor:
            val = val * scale_factor
        result.append(val)

    return result


class Origin(object):
    """Reference frame represented by an instance of :class:`Frame`."""

    @classmethod
    def from_urdf(cls, attributes, elements, text):
        xyz = _parse_floats(attributes.get('xyz', '0 0 0'), SCALE_FACTOR)
        rpy = _parse_floats(attributes.get('rpy', '0 0 0'))
        return Frame.from_euler_angles(rpy, static=True, axes='xyz', point=xyz)


class Mass(object):
    """Represents a value of mass usually related to a link."""

    def __init__(self, value):
        self.value = float(value)

    def __str__(self):
        return str(self.value)


class Inertia(object):
    """Rotational inertia matrix (3x3) represented in the inertia frame.

    Since the rotational inertia matrix is symmetric, only 6 above-diagonal
    elements of this matrix are specified here, using the attributes
    ``ixx``, ``ixy``, ``ixz``, ``iyy``, ``iyz``, ``izz``.
    """

    def __init__(self, ixx=0., ixy=0., ixz=0., iyy=0., iyz=0., izz=0.):
        # TODO: Check if we need unit conversion here (m to mm?)
        self.ixx = float(ixx)
        self.ixy = float(ixy)
        self.ixz = float(ixz)
        self.iyy = float(iyy)
        self.iyz = float(iyz)
        self.izz = float(izz)


class Inertial(object):
    """Inertial properties of a link.

    Attributes:
        origin: This is the pose of the inertial reference frame,
            relative to the link reference frame.
        mass: Mass of the link.
        inertia: 3x3 rotational inertia matrix, represented in the inertia frame.
    """

    def __init__(self, origin=None, mass=None, inertia=None):
        self.origin = origin
        self.mass = mass
        self.inertia = inertia


class Box(object):
    """3D shape primitive representing a box."""

    def __init__(self, size):
        self.size = _parse_floats(size, SCALE_FACTOR)


class Cylinder(object):
    """3D shape primitive representing a cylinder."""

    def __init__(self, radius, length):
        self.radius = float(radius) * SCALE_FACTOR
        self.length = float(length) * SCALE_FACTOR


class Sphere(object):
    """3D shape primitive representing a sphere."""

    def __init__(self, radius):
        self.radius = float(radius) * SCALE_FACTOR


class Capsule(Cylinder):
    """3D shape primitive representing a capsule."""

    def __init__(self, radius, length):
        self.radius = float(radius) * SCALE_FACTOR
        self.length = float(length) * SCALE_FACTOR


class MeshDescriptor(object):
    """Description of a mesh."""

    def __init__(self, filename, scale='1.0 1.0 1.0'):
        self.filename = filename
        self.scale = _parse_floats(scale)


class Color(object):
    """Color represented in RGBA."""

    def __init__(self, rgba):
        self.rgba = _parse_floats(rgba)


class Texture(object):
    """Texture description."""

    def __init__(self, filename):
        self.filename = filename


class Material(object):
    """Material description."""

    def __init__(self, name=None, color=None, texture=None):
        self.name = name
        self.color = color
        self.texture = texture


class Geometry(object):
    """Shape of a link."""

    def __init__(self, box=None, cylinder=None, sphere=None, capsule=None, mesh=None, **kwargs):
        self.shape = box or cylinder or sphere or capsule or mesh
        self.attr = kwargs
        if not self.shape:
            raise TypeError(
                'Geometry must define at least one of: box, cylinder, sphere, capsule, mesh')


class Visual(object):
    """Visual description of a link.

    Attributes:
        geometry: Shape of the visual element.
        origin: Reference frame of the visual element with respect
            to the reference frame of the link.
        name: Name of the visual element.
        material: Material of the visual element.
        attr: Non-standard attributes.
    """

    def __init__(self, geometry, origin=None, name=None, material=None, **kwargs):
        self.geometry = geometry
        self.origin = origin
        self.name = name
        self.material = material
        self.attr = kwargs


class Collision(object):
    """Collidable description of a link.

    Attributes:
        geometry: Shape of the collidable element.
        origin: Reference frame of the collidable element with respect
            to the reference frame of the link.
        name: Name of the collidable element.
        attr: Non-standard attributes.
    """

    def __init__(self, geometry, origin=None, name=None, **kwargs):
        self.geometry = geometry
        self.origin = origin
        self.name = name
        self.attr = kwargs


class Link(object):
    """Link represented as a rigid body with an inertia, visual, and collision features.

    Attributes:
        name: Name of the link itself.
        type: Link type. Undocumented in URDF, but used by PR2.
        visual: Visual properties of the link.
        collision: Collision properties of the link. This can be different
            from the visual properties of a link.
        inertial: Inertial properties of the link.
        attr: Non-standard attributes.
        joints: A list of joints that are the link's children
    """

    def __init__(self, name, type=None, visual=[], collision=[], inertial=None, **kwargs):
        self.name = name
        self.type = type
        self.visual = visual
        self.collision = collision
        self.inertial = inertial
        self.attr = kwargs
        self.joints = []


class ParentJoint(object):
    """Describes a parent relation between joints."""

    def __init__(self, link):
        self.link = link

    def __str__(self):
        return str(self.link)


class ChildJoint(object):
    """Describes a child relation between joints."""

    def __init__(self, link):
        self.link = link

    def __str__(self):
        return str(self.link)


class Calibration(object):
    """Reference positions of the joint, used to calibrate the absolute position."""

    def __init__(self, rising=0.0, falling=0.0, reference_position=0.0):
        self.rising = float(rising)
        self.falling = float(falling)
        self.reference_position = float(reference_position)


class Dynamics(object):
    """Physical properties of the joint used for simulation of dynamics."""

    def __init__(self, damping=0.0, friction=0.0):
        self.damping = float(damping)
        self.friction = float(friction)


class Limit(object):
    """Joint limit properties.

    Attributes:
        effort: Maximum joint effort.
        velocity: Maximum joint velocity.
        lower: Lower joint limit (radians for revolute joints, millimeter for prismatic joints).
        upper: Upper joint limit (radians for revolute joints, millimeter for prismatic joints).
    """

    def __init__(self, effort=0.0, velocity=0.0, lower=0.0, upper=0.0):
        self.effort = float(effort)
        self.velocity = float(velocity)
        # TODO: Scale upper/lower limits once this is connected to a joint, if the joint is prismatic
        self.lower = float(lower)
        self.upper = float(upper)


class Mimic(object):
    """Description of joint mimic."""

    def __init__(self, joint, multiplier=1.0, offset=0):
        self.joint = joint
        self.multiplier = multiplier
        self.offset = offset


class SafetyController(object):
    """Safety controller properties."""

    def __init__(self, k_velocity, k_position=0.0, soft_lower_limit=0.0, soft_upper_limit=0.0):
        self.k_velocity = float(k_velocity)
        self.k_position = float(k_position)
        self.soft_lower_limit = float(soft_lower_limit)
        self.soft_upper_limit = float(soft_upper_limit)


class Axis(object):
    """Representation of an axis or vector."""

    def __init__(self, xyz='0 0 0'):
        # We are not using Vector here because we
        # cannot attach _urdf_source to it due to __slots__
        xyz = _parse_floats(xyz, SCALE_FACTOR)
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]


class Joint(object):
    """Representation of the kinematics and dynamics of a
    joint and its safety limits.

    Attributes:
        name: Unique name for the joint.
        type: Joint type.
        origin: Transformation from the parent link to the child link frame.
        parent: Name of the parent link.
        child: Name of the child link.
        axis: Joint axis specified in the joint frame. Represents the axis of rotation
            for revolute joints, the axis of translation for prismatic joints, and
            the surface normal for planar joints. The axis is specified in the joint
            frame of reference.
        calibration: Reference positions of the joint, used to calibrate the absolute
            position of the joint.
        dynamics: Physical properties of the joint. These values are used to specify
            modeling properties of the joint, particularly useful for simulation.
        limit: Joint limit properties.
        safety_controller: Safety controller properties.
        mimic: Used to specify that the defined joint mimics another existing joint.
        attr: Non-standard attributes.
        childlink: the joint's child link
    """
    SUPPORTED_TYPES = ('revolute', 'continuous', 'prismatic',
                       'fixed', 'floating', 'planar')

    def __init__(self, name, type, parent, child, origin=None, axis=None, calibration=None, dynamics=None, limit=None, safety_controller=None, mimic=None, **kwargs):
        if type not in (Joint.SUPPORTED_TYPES):
            raise ValueError('Unsupported joint type: %s' % type)

        self.name = name
        self.type = type
        self.parent = parent
        self.child = child
        self.origin = origin
        self.axis = axis
        self.calibration = calibration
        self.dynamics = dynamics
        self.limit = limit
        self.safety_controller = safety_controller
        self.mimic = mimic
        self.attr = kwargs
        self.childlink = None


class Robot(object):
    """Robot is the root of the model.

    Robot instances are the root node in a urdf structure representing an entire robot.

    In line with URDF limitations, only urdf structures can be represented by this
    model, ruling out all parallel robots.

    Attributes:
        name: Unique name of the robot.
        joints: List of joint elements.
        links: List of links of the robot.
        materials: List of global materials.
        attr: Non-standard attributes.
    """

    def __init__(self, name, joints=[], links=[], materials=[], **kwargs):
        self.name = name
        self.joints = joints
        self.links = links
        self.materials = materials
        self.attr = kwargs
        # save tree structure from link and joint lists
        for link in self.links:
            link.joints = self.find_children_joints(link)
        for joint in self.joints:
            joint.childlink = self.find_child_link(joint)

    @property
    def root(self):
        if len(self.links):
            return self.find_root_link()
        else:
            return None

    @classmethod
    def from_urdf_file(cls, file):
        """Construct a Robot model from a URDF file model description.

        Args:
            file: file name or file object.

        Returns:
            A robot model instance.
        """
        return URDF.parse(file)

    @classmethod
    def from_urdf_string(cls, text):
        """Construct a Robot model from a URDF description as string.

        Args:
            text: string containing the XML URDF model.

        Returns:
            A robot model instance.
        """
        return URDF.from_string(text)

    def find_root_link(self):
        """Returns the robot's root link.

        Raises:
            Exception: If the root link of the robot could not be found.
        """
        # search the link, which is never child for a joint
        for link in self.links:
            found = False
            for joint in self.joints:
                if str(joint.child) == link.name:
                    found = True
                    break
            if not found:
                return link
        raise Exception("Root link not found. Something wrong with URDF?")

    def find_children_joints(self, link):
        """Returns a list of all children joints of the link.
        """
        joints = []
        for joint in self.joints:
            if str(joint.parent) == link.name:
                joints.append(joint)
        return joints

    def find_child_link(self, joint):
        """Returns the child link of the joint or None if not found.
        """
        for link in self.links:
            if link.name == joint.child.link:
                return link
        return None

    def find_parent_joint(self, link):
        """Returns the parent joint of the link or None if not found.
        """
        for joint in self.joints:
            if str(joint.child) == link.name:
                return joint
        return None

    def iter_links(self):
        """Returns an iterator over the links that starts with the root link.
        """
        root = self.root

        def func(cjoints, links):
            for j in cjoints:
                link = j.childlink
                links.append(link)
                links += func(link.joints, [])
            return links

        return iter(func(root.joints, [root]))

    def iter_joints(self):
        """Returns an iterator over the joints that starts with the root link's
            children joints.
        """

        def func(clink, joints):
            cjoints = clink.joints
            joints += cjoints
            for j in cjoints:
                joints += func(j.childlink, [])
            return joints

        return iter(func(self.root, []))


URDF.add_parser(Robot, 'robot')
URDF.add_parser(Joint, 'robot/joint')
URDF.add_parser(Link, 'robot/link')
URDF.add_parser(Inertial, 'robot/link/inertial')
URDF.add_parser(Mass, 'robot/link/inertial/mass')
URDF.add_parser(Inertia, 'robot/link/inertial/inertia')

URDF.add_parser(Origin, 'robot/link/inertial/origin', 'robot/link/visual/origin', 'robot/link/collision/origin', 'robot/joint/origin')

URDF.add_parser(Visual, 'robot/link/visual')
URDF.add_parser(Collision, 'robot/link/collision')

URDF.add_parser(Geometry, 'robot/link/visual/geometry', 'robot/link/collision/geometry')
URDF.add_parser(MeshDescriptor, 'robot/link/visual/geometry/mesh', 'robot/link/collision/geometry/mesh')
URDF.add_parser(Box, 'robot/link/visual/geometry/box', 'robot/link/collision/geometry/box')
URDF.add_parser(Cylinder, 'robot/link/visual/geometry/cylinder', 'robot/link/collision/geometry/cylinder')
URDF.add_parser(Sphere, 'robot/link/visual/geometry/sphere', 'robot/link/collision/geometry/sphere')
URDF.add_parser(Capsule, 'robot/link/visual/geometry/capsule', 'robot/link/collision/geometry/capsule')

URDF.add_parser(Material, 'robot/material', 'robot/link/visual/material')
URDF.add_parser(Color, 'robot/material/color', 'robot/link/visual/material/color')
URDF.add_parser(Texture, 'robot/material/texture', 'robot/link/visual/material/texture')

URDF.add_parser(ParentJoint, 'robot/joint/parent')
URDF.add_parser(ChildJoint, 'robot/joint/child')
URDF.add_parser(Calibration, 'robot/joint/calibration')
URDF.add_parser(Dynamics, 'robot/joint/dynamics')
URDF.add_parser(Limit, 'robot/joint/limit')
URDF.add_parser(Axis, 'robot/joint/axis')
URDF.add_parser(Mimic, 'robot/joint/mimic')
URDF.add_parser(SafetyController, 'robot/joint/safety_controller')
