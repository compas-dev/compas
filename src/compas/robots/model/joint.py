from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.files import URDF
from compas.geometry import Vector
from compas.geometry.transformations import transform_vectors
from compas.geometry.xforms import Rotation
from compas.geometry.xforms import Transformation

from .geometry import SCALE_FACTOR
from .geometry import Origin
from .geometry import _parse_floats

__all__ = ['Joint', 'ParentLink', 'ChildLink', 'Calibration',
           'Dynamics', 'Limit', 'Axis', 'Mimic', 'SafetyController']


class ParentLink(object):
    """Describes a parent relation between a joint its parent link."""

    def __init__(self, link):
        self.link = link

    def __str__(self):
        return str(self.link)


class ChildLink(object):
    """Describes a child relation between a joint and its child link."""

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
        xyz = _parse_floats(xyz, 1.)
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]
        self.init = None

    def copy(self):
        cls = type(self)
        return cls("%f %f %f" % (self.x, self.y, self.z))

    def reset_transform(self):
        if self.init:
            cp = self.init.copy()
            self.x = cp.x
            self.y = cp.y
            self.z = cp.z

    def transform(self, transformation):
        xyz = transform_vectors(
            [[self.x, self.y, self.z]], transformation.matrix)
        self.x = xyz[0][0]
        self.y = xyz[0][1]
        self.z = xyz[0][2]

    def create(self, transformation):
        """Stores the initial direction of the axis.
         This is called when the robot is created.
        """
        self.transform(transformation)
        self.init = self.copy()

    @property
    def vector(self):
        return Vector(self.x, self.y, self.z)

    def __str__(self):
        return "[%.3f, %.3f, %.3f]" % (self.x, self.y, self.z)


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
        child_link: the joint's child link
    """
    SUPPORTED_TYPES = ('revolute', 'continuous', 'prismatic',
                       'fixed', 'floating', 'planar')

    def __init__(self, name, type, parent, child, origin=None, axis=None, calibration=None, dynamics=None, limit=None, safety_controller=None, mimic=None, **kwargs):
        if type not in (Joint.SUPPORTED_TYPES):
            raise ValueError('Unsupported joint type: %s' % type)

        self.name = name
        self.type = type
        self.parent = parent if isinstance(parent, ParentLink) else ParentLink(parent)
        self.child = child if isinstance(child, ChildLink) else ChildLink(child)
        self.origin = origin
        self.axis = axis
        self.calibration = calibration
        self.dynamics = dynamics
        self.limit = limit
        self.safety_controller = safety_controller
        self.mimic = mimic
        self.attr = kwargs
        self.child_link = None
        self.position = 0  # the position of the joint

    @property
    def current_transformation(self):
        if self.origin:
            return Transformation.from_frame(self.origin)
        else:
            return Transformation()

    @property
    def init_transformation(self):
        if self.origin:
            return self.origin.init_transformation.copy()
        else:
            return Transformation()

    def reset_transform(self):
        if self.origin:
            self.origin.reset_transform()
        if self.axis:
            self.axis.reset_transform()

    def transform(self, transformation):
        if self.origin:
            self.origin.transform(transformation)
        if self.axis:
            self.axis.transform(transformation)

    def calculate_transformation(self, position):
        """Calculates the transformation of the joint based on the position and
        its type.
        """
        if self.type == "revolute":
            return Rotation.from_axis_and_angle(self.axis.vector, position, self.origin.point)
        elif self.type == "fixed":
            return Transformation() # identity matrix
        else:
            return NotImplementedError

    def calculate_reset_transformation(self):
        return self.init_transformation * self.current_transformation.inverse()


URDF.add_parser(Joint, 'robot/joint')
URDF.add_parser(ParentLink, 'robot/joint/parent')
URDF.add_parser(ChildLink, 'robot/joint/child')
URDF.add_parser(Calibration, 'robot/joint/calibration')
URDF.add_parser(Dynamics, 'robot/joint/dynamics')
URDF.add_parser(Limit, 'robot/joint/limit')
URDF.add_parser(Axis, 'robot/joint/axis')
URDF.add_parser(Mimic, 'robot/joint/mimic')
URDF.add_parser(SafetyController, 'robot/joint/safety_controller')

URDF.add_parser(Origin, 'robot/joint/origin')
