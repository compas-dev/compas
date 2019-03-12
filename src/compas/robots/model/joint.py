from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.files import URDFParser
from compas.geometry import Vector
from compas.geometry import transform_vectors
from compas.geometry import Rotation
from compas.geometry import Transformation
from compas.geometry import Translation

from compas.robots.model.geometry import Origin
from compas.robots.model.geometry import _parse_floats


__all__ = [
    'Joint',
    'ParentLink',
    'ChildLink',
    'Calibration',
    'Dynamics',
    'Limit',
    'Axis',
    'Mimic',
    'SafetyController'
]


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
        lower: Lower joint limit (radians for revolute joints, meter for
            prismatic joints).
        upper: Upper joint limit (radians for revolute joints, meter for
            prismatic joints).
    """

    def __init__(self, effort=0.0, velocity=0.0, lower=0.0, upper=0.0):
        self.effort = float(effort)
        self.velocity = float(velocity)
        self.lower = float(lower)
        self.upper = float(upper)

    def scale(self, factor):
        self.lower *= factor
        self.upper *= factor


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

    def __init__(self, xyz='0 0 0', **kwargs):
        # We are not using Vector here because we
        # cannot attach _urdf_source to it due to __slots__
        xyz = _parse_floats(xyz)
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]
        self.attr = kwargs

    def copy(self):
        cls = type(self)
        return cls("%f %f %f" % (self.x, self.y, self.z))

    def transform(self, transformation):
        xyz = transform_vectors(
            [[self.x, self.y, self.z]], transformation.matrix)
        self.x = xyz[0][0]
        self.y = xyz[0][1]
        self.z = xyz[0][2]

    @property
    def vector(self):
        return Vector(self.x, self.y, self.z)

    def __str__(self):
        return "[%.3f, %.3f, %.3f]" % (self.x, self.y, self.z)


class Joint(object):
    """Representation of the kinematics and dynamics of a joint and its safety
    limits.

    Attributes:
        name: Unique name for the joint.
        type: Joint type.
        origin: Transformation from the parent link to the child link frame.
        parent: Name of the parent link.
        child: Name of the child link.
        axis: Joint axis specified in the joint frame. Represents the axis of
            rotation for revolute joints, the axis of translation for prismatic
            joints, and the surface normal for planar joints. The axis is
            specified in the joint frame of reference.
        calibration: Reference positions of the joint, used to calibrate the
            absolute position of the joint.
        dynamics: Physical properties of the joint. These values are used to
            specify modeling properties of the joint, particularly useful for
            simulation.
        limit: Joint limit properties.
        safety_controller: Safety controller properties.
        mimic: Used to specify that the defined joint mimics another existing
            joint.
        attr: Non-standard attributes.
        child_link: the joint's child link
        position (float): The current position of the joint. This depends on the
            joint type, i.e. for revolute joints, it will be the rotation angle
            in radians, for prismatic joints the translation in meters.
    """

    REVOLUTE = 0
    CONTINUOUS = 1
    PRISMATIC = 2
    FIXED = 3
    FLOATING = 4
    PLANAR = 5

    SUPPORTED_TYPES = ('revolute', 'continuous', 'prismatic', 'fixed',
                       'floating', 'planar')

    def __init__(self, name, type, parent, child, origin=None, axis=None, calibration=None, dynamics=None, limit=None, safety_controller=None, mimic=None, **kwargs):
        if type not in (Joint.SUPPORTED_TYPES):
            raise ValueError('Unsupported joint type: %s' % type)

        self.name = name
        self.type = Joint.SUPPORTED_TYPES.index(type)
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
        self.position = 0
        self.init_origin = origin.copy() if origin else None
        self.init_axis = axis.copy() if axis else None

        switcher = {
            Joint.REVOLUTE: self.calculate_revolute_transformation,
            Joint.CONTINUOUS: self.calculate_continous_transformation,
            Joint.PRISMATIC: self.calculate_prismatic_transformation,
            Joint.FIXED: self.calculate_fixed_transformation,
            Joint.FLOATING: self.calculate_floating_transformation,
            Joint.PLANAR: self.calculate_planar_transformation
        }
        # set the transformation function according to the type
        self.calculate_transformation = switcher.get(self.type)

    @property
    def current_transformation(self):
        if self.origin:
            return Transformation.from_frame(self.origin)
        else:
            return Transformation()

    @property
    def init_transformation(self):
        if self.init_origin:
            return Transformation.from_frame(self.init_origin)
        else:
            return Transformation()

    @property
    def reset_transformation(self):
        return self.init_transformation * self.current_transformation.inverse()

    def reset_transform(self):
        if self.init_origin:
            self.origin = self.init_origin.copy()
        if self.init_axis:
            self.axis = self.init_axis.copy()

    def transform(self, transformation):
        if self.origin:
            self.origin.transform(transformation)
        if self.axis:
            self.axis.transform(transformation)

    def create(self, transformation):
        if self.origin:
            self.origin.transform(transformation)
            self.init_origin = self.origin.copy()
        if self.axis:
            self.axis.transform(self.current_transformation)
            self.init_axis = self.axis.copy()

    def calculate_revolute_transformation(self, position):
        """Returns a transformation of a revolute joint.

        A revolute joint rotates about the axis and has a limited range
        specified by the upper and lower limits.

        Args:
            position (float): the angle in radians
        """
        position = max(min(position, self.limit.upper), self.limit.lower)
        return self.calculate_continous_transformation(position)

    def calculate_continous_transformation(self, position):
        """Returns a transformation of a continous joint.

        A continous joint rotates about the axis and has no upper and lower
        limits.

        Args:
            position (float): the angle in radians
        """
        return Rotation.from_axis_and_angle(self.axis.vector, position, self.origin.point)

    def calculate_prismatic_transformation(self, position):
        """Returns a transformation of a prismatic joint.

        A prismatic joint slides along the axis and has a limited range
        specified by the upper and lower limits.

        Args:
            position (float): the movement in meters.
        """
        position = max(min(position, self.limit.upper), self.limit.lower)
        return Translation(self.axis.vector * position)

    # does this ever happen?
    def calculate_fixed_transformation(self, position):
        """Returns an identity transformation.

        The fixed joint is is not really a joint because it cannot move. All
        degrees of freedom are locked.
        """
        return Transformation()

    def calculate_floating_transformation(self, position):
        """Returns a transformation of a floating joint.

        A floating joint allows motion for all 6 degrees of freedom.
        """
        raise NotImplementedError

    def calculate_planar_transformation(self, position):
        """Returns a transformation of a planar joint.

        A planar joint allows motion in a plane perpendicular to the axis.
        """
        raise NotImplementedError

    def calculate_transformation(self, position):
        """Returns the transformation of the joint.

        This function is overwitten in the init based on the joint type.

        Args:
            position (float): radians or meters.
        """
        pass

    def is_configurable(self):
        """Returns ``True`` if the joint can be configured, otherwise ``False``."""
        return self.type != Joint.FIXED
    
    def is_scalable(self):
        """Returns ``True`` if the joint can be scaled, otherwise ``False``."""
        return self.type in [Joint.PLANAR, Joint.PRISMATIC]

    def scale(self, factor):
        self.origin.scale(factor)
        self.init_origin.point *= factor
        if self.is_scalable():
            self.limit.scale(factor)



URDFParser.install_parser(Joint, 'robot/joint')
URDFParser.install_parser(ParentLink, 'robot/joint/parent')
URDFParser.install_parser(ChildLink, 'robot/joint/child')
URDFParser.install_parser(Calibration, 'robot/joint/calibration')
URDFParser.install_parser(Dynamics, 'robot/joint/dynamics')
URDFParser.install_parser(Limit, 'robot/joint/limit')
URDFParser.install_parser(Axis, 'robot/joint/axis')
URDFParser.install_parser(Mimic, 'robot/joint/mimic')
URDFParser.install_parser(SafetyController, 'robot/joint/safety_controller')

URDFParser.install_parser(Origin, 'robot/joint/origin')
