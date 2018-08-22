from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.files import URDF as SRDF

from compas.robots.model.geometry import SCALE_FACTOR
from compas.robots.model.geometry import _parse_floats


"""
http://docs.ros.org/kinetic/api/srdfdom/html/srdf_8py_source.html
"""

class Group(object):
    """Representation of a set of joints and links. 
    
    Attributes:
        name (str): is the name of the group
        link:
        joint:
        chain:
        group:

    Note: 
        If a group contains no tags, only its name attribute, it is assumed to
        be a reference to a group with that name, but that is defined earlier.
    """
    def __init__(self, name=None, links=[], joints=[], chains=[], groups=[]):
        self.name = name
        self.links = links
        self.joints = joints
        self.chains = chains
        self.groups = groups
    
    def get_link_count(self):
        return len(self.get_link_names())

    def get_link_names(self, urdf_model):
        link_names = []
        if len(self.links):
            for link in self.links:
                link_names.append(link.name)        
        if len(self.chains):
            for chain in self.chains:
                for link in urdf_model.iter_link_chain(chain.base_link, chain.tip_link):
                    link_names.append(link.name)
        if len(self.joints):
            for joint in self.joints:
                # TODO
                pass
        if len(self.groups):
            for group in self.groups:
                link_names += group.get_link_names()
        return list(set(link_names)) # unique list

class GroupState(object):
    """Defines a named state for a particular group, in terms of joint values.

    Attributes:
        name (str): is the name of the state
        group (str): is the name of the group the state is for
        joint (list): 

    Note: 
        All joints in a group must have their value specified as part of a group
        state in order for that state to be valid.
    """
    def __init__(self, name=None, group=None, joints=[]):
        self.name = name
        self.group = group
        self.joints = joints

class Link(object):
    """This element specifies a link that is part of a class::`Group`.

    Attributes:
        name (str): must be a name of a link in the corresponding URDF file

    Note: 
        If a link is included in a group, so is the corresponding parent joint 
        (if one exists).
    """
    def __init__(self, name=None):
        self.name = name

class Joint(object):
    """This element specifies a joint that is part of a class::`Group`.

    Attributes:
        name (str): must be a name of a joint in the corresponding URDF file
        value (float): *only* in the <group_state> tag, the value attribute is 
            accepted for joints. If a joint consists of multiple DOF, the value
            is simply a space-separated array of floating point values.
    
    Note:
        If a joint is included in a group, so is the corresponding child link.
    """
    def __init__(self, name=None, value=[]):
        self.name = name
        self.value = value


class Chain(object):
    """Represent a kinematic chain in the robot.

    Attributes:
        base_link: is the root link of the chain (the link that is fixed with 
            respect to the chain)
        tip_link: is the last link of the chain (where the chain ends)

    Note:
        Based on the links in the chain, the set of joints in the chain is 
        implicitly defined. The joints that correspond to a chain are the parent
        joints for the links in the chain, except the parent joint of the 
        base_link.
    """
    def __init__(self, base_link=None, tip_link=None):
        self.base_link = base_link
        self.tip_link = tip_link

class EndEffector(object):
    """Represent information about an end effector.

    Attributes:
        name: is the name of the end effector
        group: is the name of the group that contains the links (and joints)
            that make up the end effector
        parent_link: is the name of the link this end effector is attached to
        parent_group: (optional) is the name of a group containing parent_link.
    """
    def __init__(self, name=None, group=None, parent_link=None, parent_group=None):
        self.name = name
        self.group = group
        self.parent_link = parent_link
        self.parent_group = parent_group

class VirtualJoint(object):
    """This element defines a virtual joint between a robot link and an external
    frame of reference (considered fixed with respect to the robot).

    Attributes:
        name (str): the name of the joint that is assumed to exist between the
            robot and the environment
        child_link (str): the name of the link that connects the robot to the 
            environment
        parent_frame (str): the name of the frame assumed to be fixed with
            respect to the robot
        type (str): the type of joint to be assumed. This can be fixed (0 DOF), 
            floating (all 6 DOF) or planar (3 DOF: x, y, yaw)
    
    Note:
        If the <joint> tag is used to refer to existing joints by name, using 
        the name of defined virtual joints is also possible.
    """

    TYPES = ['unknown', 'fixed', 'floating', 'planar']

    def __init__(self, name=None, child_link=None, parent_frame=None, type=None):
        self.name = name
        self.child_link = child_link
        self.parent_frame = parent_frame
        self.type = type
    
    def check_valid(self):
        assert self.type in self.TYPES, "Invalid joint type: {}".format(self.type)


class DisableCollisions(object):
    """Defines disabled collisions between joints.
    
    By default it is assumed that any link of the robot could potentially 
    come into collision with any other link in the robot. This tag disables
    collision checking between a specified pair of links.

    Attributes:
        link1 (str): the name of the first link in the pair
        link2 (str): the name of the second link in the pair
        reason (str): (optional) the reason this collisions between the two links 
            should be disabled.
    """
    def __init__(self, link1=None, link2=None, reason=None):
        self.link1 = link1
        self.link2 = link2
        self.reason = reason

class PassiveJoint(object):
    """Specifies a `Joint` that is passive.
    
    By default it is assumed that all joints specified by a URDF are active and
    their state is made available for planning. If this is not the case for some
    joints, this tag can be used to specify that.

    Attributes:
        name (str): the name of the joint that is passive.
    """
    def __init__(self, name=None):
        self.name = name

class LinkSphereApproximation(object):
    """Specifies a set of spheres that conservatively approximates a link.
    
    Spheres are specified in the same coordinate frame as the collision geometry
    in the URDF. This tag is optional. If no tag appears for a link then a 
    single sphere that encloses the link's collision geometry will be used.
    If a tag appears and contains only spheres with radius 0 then the link will
    not be considered when doing sphere based collision detection.

    Attributes:
        link (str): the name of the link that is approximated by these spheres.
        sphere:
    """
    def __init__(self, spheres=[], link=''):
        self.spheres = spheres
        self.link = link

class Sphere(object):
    """Specifies a sphere.

    Attributes:
        center (list): 3 values specifying the sphere center.
        radius (float): a floating point sphere radius.
    """
    def __init__(self, center=[], radius=0):
        self.center = center
        self.radius = radius
    
    @classmethod
    def from_urdf(cls, attributes, elements, text):
        center = _parse_floats(attributes.get('center', '0 0 0'), SCALE_FACTOR)
        radius = _parse_floats(attributes.get('radius', '0'))
        return cls(center, radius)


class Robot(object):
    """Robot is the root element of the semantic.

    Attributes:
        name (str): The name of the robot.
        groups:
        end_effectors:
        virtual_joints:
        group_states: 
        disable_collisionss:
    """
    def __init__(self, name, groups=[], end_effectors=[], virtual_joints=[], 
                 group_state=[], disable_collisionss=[], passive_joints=[], 
                 link_sphere_approximations=[], urdf_model=None):
            self.name = name
            self.groups = groups
            self.end_effectors = end_effectors
            self.virtual_joints = virtual_joints
            self.group_state = group_state
            self.disable_collisionss = disable_collisionss
            self.passive_joints = passive_joints
            self.link_sphere_approximations = link_sphere_approximations
            self.urdf_model = urdf_model
    
    def set_urdf_model(urdf_model):
        self.urdf_model = urdf_model

    @classmethod
    def from_srdf_file(cls, file):
        """Construct Robot semantics from a SRDF file.

        Args:
            file: file name or file object.

        Returns:
            A Robot semantics instance.
        """
        return SRDF.parse(file)

    @classmethod
    def from_srdf_string(cls, text):
        """Construct Robot semantics from a SRDF string.

        Args:
            text (str): string containing the XML SRDF.

        Returns:
            A Robot semantics instance.
        """
        return SRDF.from_string(text)
    
    def get_planning_groups(self):
        return [group.name for group in self.groups]
    
    def get_main_planning_group(self):
        """Returns the name of the planning group with the highest number of 
            links.
        """
        assert self.urdf_model, "urdf_model must be set."

        for group in self.groups:
            num_links = group.get_link_count(self.urdf_model)

SRDF.add_parser(Robot, 'robot')
SRDF.add_parser(Group, 'robot/group')
SRDF.add_parser(Chain, 'robot/group/chain')
SRDF.add_parser(Link, 'robot/group/link')
SRDF.add_parser(Joint, 'robot/group/joint')
SRDF.add_parser(Group, 'robot/group/group')
SRDF.add_parser(EndEffector, 'robot/end_effector')
SRDF.add_parser(GroupState, 'robot/group_state')
SRDF.add_parser(Joint, 'robot/group_state/joint')
SRDF.add_parser(VirtualJoint, 'robot/virtual_joint')
SRDF.add_parser(DisableCollisions, 'robot/disable_collisions')
SRDF.add_parser(LinkSphereApproximation, 'robot/link_sphere_approximation')
SRDF.add_parser(Sphere, 'robot/link_sphere_approximation/sphere')
SRDF.add_parser(PassiveJoint, 'robot/passive_joint')
