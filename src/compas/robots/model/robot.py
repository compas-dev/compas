from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import random

import compas
from compas.data import Data
from compas.datastructures import Mesh
from compas.files import URDF
from compas.files import URDFElement
from compas.files import URDFParser
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.robots import Configuration
from compas.robots.model.base import _attr_from_data
from compas.robots.model.base import _attr_to_data
from compas.robots.model.geometry import Color
from compas.robots.model.geometry import Geometry
from compas.robots.model.geometry import Material
from compas.robots.model.geometry import MeshDescriptor
from compas.robots.model.geometry import Texture
from compas.robots.model.joint import Axis
from compas.robots.model.joint import Joint
from compas.robots.model.joint import Limit
from compas.robots.model.link import Collision
from compas.robots.model.link import Link
from compas.robots.model.link import Visual
from compas.robots.resources import DefaultMeshLoader
from compas.robots.resources import LocalPackageMeshLoader
from compas.topology import shortest_path

__all__ = ['RobotModel']


class RobotModel(Data):
    """RobotModel is the root element of the model.

    Instances of this class represent an entire robot as defined in an URDF
    structure.

    In line with URDF limitations, only tree structures can be represented by
    this model, ruling out all parallel robots.

    Attributes
    ----------
    name : str
        Unique name of the robot.
    joints : list[:class:`~compas.robots.Joint`]
        List of joint elements.
    links : list[:class:`~compas.robots.Link`]
        List of links of the robot.
    materials : list[:class:`~compas.robots.Material`]
        List of global materials.
    root : :class:`~compas.robots.Link`
        Root link of the model.
    attr : dict
        Non-standard attributes.

    """

    def __init__(self, name=None, joints=(), links=(), materials=(), **kwargs):
        super(RobotModel, self).__init__()
        self.name = name or 'Robot'
        self.joints = list(joints or [])
        self.links = list(links or [])
        self.materials = list(materials or [])
        self.attr = kwargs
        self.root = None
        self._rebuild_tree()
        self._create(self.root, Transformation())
        self._scale_factor = 1.

    def get_urdf_element(self):
        attributes = {'name': self.name}
        attributes.update(self.attr)
        elements = self.links + self.joints + self.materials
        return URDFElement('robot', attributes, elements)

    @property
    def data(self):
        """Returns the data dictionary that represents the :class:`RobotModel`.

        Returns
        -------
        dict
            The RobotModel's data.

        """
        return self._get_data()

    def _get_data(self):
        return {
            'name': self.name,
            'joints': [joint.data for joint in self.joints],
            'links': [link.data for link in self.links],
            'materials': [material.data for material in self.materials],
            'attr': _attr_to_data(self.attr),
            '_scale_factor': self._scale_factor,
        }

    @data.setter
    def data(self, data):
        self._set_data(data)

    def _set_data(self, data):
        self.name = data.get('name', '')
        self.joints = [Joint.from_data(d) for d in data.get('joints', [])]
        self.links = [Link.from_data(d) for d in data.get('links', [])]
        self.materials = [Material.from_data(d) for d in data.get('materials', [])]
        self.attr = _attr_from_data(data.get('attr', {}))
        self._scale_factor = data.get('_scale_factor', 1.)

        self._rebuild_tree()

    def _rebuild_tree(self):
        """Store tree structure from link and joint lists."""
        self._adjacency = dict()
        self._links = dict()
        self._joints = dict()

        for link in self.links:
            link.joints = self.find_children_joints(link)
            link.parent_joint = self.find_parent_joint(link)

            self._links[link.name] = link
            self._adjacency[link.name] = [joint.name for joint in link.joints]

            if not link.parent_joint:
                self.root = link

        for joint in self.joints:
            child_name = joint.child.link
            joint.child_link = self.get_link_by_name(child_name)

            self._joints[joint.name] = joint
            self._adjacency[joint.name] = [child_name]

    @classmethod
    def from_urdf_file(cls, file):
        """Construct a robot model from a URDF file model description.

        Parameters
        ----------
        file : str | file
            File path or file-like object.

        Returns
        -------
        :class:`~compas.robots.RobotModel`
            A robot model instance.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> print(robot)
        Robot name=ur5, Links=11, Joints=10 (6 configurable)

        """
        urdf = URDF.from_file(file)
        return urdf.robot

    def to_urdf_file(self, file, prettify=False):
        """Construct a URDF file model description from a robot model.

        Parameters
        ----------
        file : str | file
            File path or file-like object.

        Returns
        -------
        None

        """
        urdf = URDF.from_robot(self)
        urdf.to_file(file, prettify)

    @classmethod
    def from_urdf_string(cls, text):
        """Construct a robot model from a URDF description as string.

        Parameters
        ----------
        text : str
            String containing the XML URDF model.

        Returns
        -------
        :class:`~compas.robots.RobotModel`
            A robot model instance.

        Examples
        --------
        >>> urdf_string = '<?xml version="1.0" encoding="UTF-8"?><robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="panda"></robot>'
        >>> robot = RobotModel.from_urdf_string(urdf_string)

        """
        urdf = URDF.from_string(text)
        return urdf.robot

    @classmethod
    def ur5(cls, load_geometry=False):
        """"Construct a UR5 robot model.

        Parameters
        ----------
        load_geometry : bool, optional
            Indicate whether to load the geometry of the robot or not.

        Returns
        -------
        :class:`~compas.robots.RobotModel`
            A robot model instance.

        """
        model = cls.from_urdf_file(compas.get('ur_description/urdf/ur5.urdf'))
        if load_geometry:
            loader = LocalPackageMeshLoader(compas.DATA, 'ur_description')
            model.load_geometry(loader)
        return model

    def to_urdf_string(self, prettify=False):
        """Construct a URDF string model description from a robot model.

        Parameters
        ----------
        prettify : bool, optional
            If True, the string will be pretty-printed.

        Returns
        -------
        str
            URDF string.

        """
        urdf = URDF.from_robot(self)
        return urdf.to_string(prettify=prettify)

    def find_children_joints(self, link):
        """Returns a list of all children joints of the link.
        """
        joints = []
        for joint in self.joints:
            if str(joint.parent) == link.name:
                joints.append(joint)
        return joints

    def find_parent_joint(self, link):
        """Returns the parent joint of the link or None if not found.

        Parameters
        ----------
        link : :class:`~compas.robots.Link`
            The link of which we want to know the parent joint.

        Returns
        -------
        :class:`~compas.robots.Joint`
            The parent joint of the link.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> j = robot.find_parent_joint(Link('shoulder_link'))
        >>> j.name
        'shoulder_pan_joint'

        """
        for joint in self.joints:
            if str(joint.child) == link.name:
                return joint
        return None

    def get_link_by_name(self, name):
        """Get a link in a robot model matching by its name.

        Parameters
        ----------
        name : str
            Link name.

        Returns
        -------
        :class:`~compas.robots.Link`
            A link instance.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> l = robot.get_link_by_name('world')
        >>> l.name
        'world'

        """
        return self._links.get(name, None)

    def get_joint_by_name(self, name):
        """Get a joint in a robot model matching by its name.

        Parameters
        ----------
        name : str
            Joint name.

        Returns
        -------
        :class:`Joint`
            A joint instance.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> j = robot.get_joint_by_name('shoulder_lift_joint')
        >>> j.name
        'shoulder_lift_joint'

        """
        return self._joints.get(name, None)

    def iter_links(self):
        """Iterator over the links that starts with the root link.

        Returns
        -------
        Iterator of all links starting at root.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> [l.name for l in robot.iter_links()]
        ['world', 'base_link', 'shoulder_link', 'upper_arm_link', 'forearm_link', 'wrist_1_link', 'wrist_2_link', 'wrist_3_link', 'ee_link', 'tool0', 'base']

        """

        def func(cjoints, links):
            for j in cjoints:
                link = j.child_link
                links.append(link)
                links += func(link.joints, [])
            return links

        return iter(func(self.root.joints, [self.root]))

    def iter_joints(self):
        """Iterator over the joints that starts with the root link's children joints.

        Returns
        -------
        Iterator of all joints starting at root.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> [j.name for j in robot.iter_joints()]
        ['world_joint', 'shoulder_pan_joint', 'base_link-base_fixed_joint', 'shoulder_lift_joint', \
        'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint', 'ee_fixed_joint', 'wrist_3_link-tool0_fixed_joint']

        """

        def func(clink, joints):
            cjoints = clink.joints
            joints += cjoints
            for j in cjoints:
                joints += func(j.child_link, [])
            return joints

        return iter(func(self.root, []))

    def iter_link_chain(self, link_start_name=None, link_end_name=None):
        """Iterator over the chain of links between a pair of start and end links.

        Parameters
        ----------
        link_start_name : str, optional
            Name of the starting link of the chain. Defaults to the root link name.
        link_end_name : str, optional
            Name of the final link of the chain. Defaults to the last link's name.

        Returns
        -------
        Iterator of the chain of links.

        Notes
        -----
        This method differs from :meth:`iter_links` in that it returns the chain respecting
        the tree structure, hence if one link branches into two or more joints, only the
        branch matching the end link will be returned.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> [l.name for l in robot.iter_link_chain('world', 'forearm_link')]
        ['world', 'base_link', 'shoulder_link', 'upper_arm_link', 'forearm_link']

        """
        chain = self.iter_chain(link_start_name, link_end_name)
        for link in map(self.get_link_by_name, chain):
            # If None, it's not a link
            if link:
                yield link

    def iter_joint_chain(self, link_start_name=None, link_end_name=None):
        """Iterator over the chain of joints between a pair of start and end links.

        Parameters
        ----------
        link_start_name : str, optional
            Name of the starting link of the chain. Defaults to the root link name.
        link_end_name : str, optional
            Name of the final link of the chain. Defaults to the last link's name.

        Returns
        -------
        Iterator of the chain of joints.

        Notes
        -----
        This method differs from :meth:`iter_joints` in that it returns the
        chain respecting the tree structure, hence if one link branches into
        two or more joints, only the branch matching the end link will be
        returned.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> [j.name for j in robot.iter_joint_chain('world', 'forearm_link')]
        ['world_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint']

        """
        chain = self.iter_chain(link_start_name, link_end_name)
        for joint in map(self.get_joint_by_name, chain):
            # If None, it's not a joint
            if joint:
                yield joint

    def iter_chain(self, start=None, end=None):
        """Iterator over the chain of all elements between a pair of start and end elements.

        Parameters
        ----------
        start : str, optional
            Name of the starting element of the chain. Defaults to the root link name.
        end : str, optional
            Name of the final element of the chain. Defaults to the name of the last element.

        Returns
        -------
        Iterator of the chain of links and joints (names).

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> list(robot.iter_chain('world', 'forearm_link'))
        ['world', 'world_joint', 'base_link', 'shoulder_pan_joint', 'shoulder_link', 'shoulder_lift_joint', 'upper_arm_link', 'elbow_joint', 'forearm_link']

        """
        if not start:
            if not self.root:
                raise Exception('No root link found')
            start = self.root.name

        if not end:
            # Normally URDF will contain the end links at the end
            # so we break out faster by reversing the list
            for link in reversed(self.links):
                if not link.joints:
                    end = link.name
                    break

        shortest_chain = shortest_path(self._adjacency, start, end)

        if not shortest_chain:
            raise Exception('No chain found between the specified element')

        for name in shortest_chain:
            yield name

    def get_configurable_joints(self):
        """Returns the configurable joints.

        Configurable joints are those that are not FIXED or MIMIC.

        Returns
        -------
        list[:class:`~compas.robots.Joint`]
            List of configurable joints.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> joints = robot.get_configurable_joints()
        >>> [j.name for j in joints]
        ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

        """
        joints = self.iter_joints()
        return [joint for joint in joints if joint.is_configurable()]

    def get_joint_types(self):
        """Returns the joint types of the configurable joints.

        Returns
        -------
        list[int]
            List of joint types in the robot model.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> robot.get_joint_types() == [Joint.REVOLUTE] * 6
        True

        """
        joints = self.get_configurable_joints()
        return [joint.type for joint in joints]

    def get_joint_types_by_names(self, names):
        """Get a list of joint types given a list of joint names.

        Parameters
        ----------
        names : list[str]
            The names of the joints.

        Returns
        -------
        list[:attr:`compas.robots.Joint.SUPPORTED_TYPES`]
            List of joint types.

        """
        return [self.get_joint_by_name(n).type for n in names]

    def get_configurable_joint_names(self):
        """Returns the configurable joint names.

        Returns
        -------
        list[str]
            List of configurable joint names.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> robot.get_configurable_joint_names()
        ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']

        """
        joints = self.get_configurable_joints()
        return [j.name for j in joints]

    def get_end_effector_link(self):
        """Returns the end effector link.

        Returns
        -------
        :class:`~compas.robots.Link`
            Instance of the end effector link.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> link = robot.get_end_effector_link()
        >>> link.name
        'ee_link'

        """
        joints = self.get_configurable_joints()
        clink = joints[-1].child_link
        for j in clink.joints:
            if j.type == Joint.FIXED:
                return j.child_link
        return clink

    def get_end_effector_link_name(self):
        """Returns the name of the end effector link.

        Returns
        -------
        str
            Name of the end effector link

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> robot.get_end_effector_link_name()
        'ee_link'

        """
        link = self.get_end_effector_link()
        return link.name

    def get_base_link_name(self):
        """Returns the name of the base link.

        Returns
        -------
        str
            Name of the base link

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> robot.get_base_link_name()
        'base_link'

        """
        joints = self.get_configurable_joints()
        return joints[0].parent.link

    def zero_configuration(self):
        """Get the zero joint configuration.

        If zero is out of joint limits ``(upper, lower)`` then
        ``(upper + lower) / 2`` is used as joint value.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> robot.zero_configuration()
        Configuration((0.000, 0.000, 0.000, 0.000, 0.000, 0.000), (0, 0, 0, 0, 0, 0), \
            ('shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint'))

        """
        values = []
        joint_names = []
        joint_types = []
        for joint in self.get_configurable_joints():
            if joint.limit and not (0 <= joint.limit.upper and 0 >= joint.limit.lower):
                values.append((joint.limit.upper + joint.limit.lower)/2.)
            else:
                values.append(0)
            joint_names.append(joint.name)
            joint_types.append(joint.type)
        return Configuration(values, joint_types, joint_names)

    def random_configuration(self):
        """Get a random configuration.

        Returns
        -------
        :class:`~compas.robots.Configuration`
            Instance of a configuration with randomized joint values.

        Note
        ----
        No collision checking is involved, the configuration may be invalid.

        """
        configurable_joints = self.get_configurable_joints()
        values = []
        for joint in configurable_joints:
            if joint.limit:
                values.append(joint.limit.lower + (joint.limit.upper - joint.limit.lower) * random.random())
            else:
                values.append(0)
        joint_names = self.get_configurable_joint_names()
        joint_types = self.get_joint_types_by_names(joint_names)
        return Configuration(values, joint_types, joint_names)

    def load_geometry(self, *resource_loaders, **kwargs):
        """Load external geometry resources, such as meshes.

        Parameters
        ----------
        resource_loaders : :class:`~compas.robots.AbstractMeshLoader`
            List of objects that implement the
            resource loading interface (:class:`~compas.robots.AbstractMeshLoader`)
            and can retrieve external geometry.
        force : bool
            True if it should force reloading even if the geometry
            has been loaded already, otherwise False.


        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> robot.load_geometry(LocalPackageMeshLoader(compas.DATA, 'ur_description'))
        >>> print(robot)
        Robot name=ur5, Links=11, Joints=10 (6 configurable)

        """
        force = kwargs.get('force', False)

        loaders = list(resource_loaders)
        loaders.insert(0, DefaultMeshLoader())

        for link in self.links:
            for element in itertools.chain(link.collision, link.visual):
                shape = element.geometry.shape
                needs_reload = force or not shape.meshes
                if 'filename' in dir(shape) and needs_reload:
                    for loader in loaders:
                        if loader.can_load_mesh(shape.filename):
                            # NOTE: this part is annoying, but we keep it for backwards compatibility's sake.
                            # Externally defined loaders (eg. COMPAS_FAB File Server loader)
                            # might not be updated yet on the user's system, so we fallback
                            # to the deprecated load_mesh method in that case.
                            # However, to add to the confusion, some loaders were actually returning
                            # meshes regardless of the misnaming. We handle that in _get_item_meshes
                            # so, we don't force load_mesh into a list, otherwise it will turn into a
                            # list of lists in those cases.
                            # All of this ugly fallback should be removed in 2.0
                            if hasattr(loader, 'load_meshes'):
                                shape.meshes = loader.load_meshes(shape.filename)
                            else:
                                shape.meshes = loader.load_mesh(shape.filename)
                            break

                    if not shape.meshes:
                        raise Exception('Unable to load meshes for {}'.format(shape.filename))

    def ensure_geometry(self):
        """Check if geometry has been loaded.

        Raises
        ------
        :exc:`Exception`
            If geometry has not been loaded.

        """
        for link in self.links:
            for element in itertools.chain(link.collision, link.visual):
                shape = element.geometry.shape
                if not shape.meshes:
                    raise Exception(
                        'This method is only callable once the geometry has been loaded.')

    @property
    def frames(self):
        """Returns the frames of links that have a visual node.

        Returns
        -------
        list[:class:`~compas.geometry.Frame`]
            Reference frames of all links with a visual representation.

        """
        frames = []
        for link in self.iter_links():
            if len(link.visual) and link.parent_joint:
                frames.append(link.parent_joint.current_origin.copy())
        return frames

    @property
    def axes(self):
        """Returns the joints' axes.

        Returns
        -------
        list[:class:`Vector`]
            Axis vectors of all joints.

        """
        axes = []
        for joint in self.iter_joints():
            axes.append(joint.current_axis.vector)
        return axes

    def __str__(self):
        """Generate a readable representation of the robot."""
        return 'Robot name={}, Links={}, Joints={} ({} configurable)'.format(
            self.name,
            len(self.links),
            len(self.joints),
            len(self.get_configurable_joints()),
        )

    def _create(self, link, parent_transformation):
        """Private function called during initialization to transform origins and axes.

        Parameters
        ----------
        link : :class:`~compas.robots.Link`
            Link instance to create.
        parent_transformation : :class:`Transformation`
            Parent transformation to apply to the link when creating the structure.

        """
        if link is None:  # some urdfs would fail here otherwise
            return

        for item in itertools.chain(link.visual, link.collision):
            if item.origin:
                # transform visual or collision geometry with the transformation specified in origin
                transformation = Transformation.from_frame(item.origin)
                item.init_transformation = parent_transformation * transformation
            else:
                item.init_transformation = parent_transformation

        for child_joint in link.joints:
            child_joint._create(parent_transformation)
            # Recursively call creation
            self._create(child_joint.child_link, child_joint.current_transformation)

    def scale(self, factor, link=None):
        """Scales the robot by factor (absolute).

        Parameters
        ----------
        factor : float
            The factor to scale the robot with.
        link : :class:`~compas.robots.Link`, optional
            Starting link from which to start scaling.
            Defaults to root.

        Returns
        -------
        None

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> robot.scale(100)

        """
        if not link or link == self.root:
            link = self.root
            relative_factor = factor / self._scale_factor  # relative scaling factor
        else:
            relative_factor = factor

        for child_joint in link.joints:
            child_joint.scale(relative_factor)
            # Recursive call
            self.scale(relative_factor, child_joint.child_link)

        self._scale_factor = factor

    def compute_transformations(self, joint_state, link=None, parent_transformation=None):
        """Recursive function to calculate the transformations of each joint.

        Parameters
        ----------
        joint_state : :class:`~compas.robots.Configuration` | dict[str, float]
            A configuration instance or a dictionary with joint names and joint values in radians and
            meters (depending on the joint type).
        link : :class:`~compas.robots.Link`, optional
            Link instance to calculate the child joint's transformation.
        parent_transformation : :class:`Transformation`, optional
            The transfomation of the parent joint.
            Defaults to the identity matrix.

        Returns
        -------
        dict[str, :class:`Transformation`]
            A dictionary with the joint names as keys and values are the joint's respective transformation.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> config = robot.random_configuration()
        >>> transformations = robot.compute_transformations(config)

        """
        if link is None:
            link = self.root
        if parent_transformation is None:
            parent_transformation = Transformation()

        transformations = {}

        for child_joint in link.joints:
            if child_joint.name in joint_state.keys():  # if passive/mimicking joint is in the joint_state, the transformation will be calculated according to this value
                position = joint_state[child_joint.name]
                transformation = parent_transformation * child_joint.calculate_transformation(position)
            elif child_joint.mimic and child_joint.mimic.joint in joint_state.keys():
                mimicked_joint_position = joint_state[child_joint.mimic.joint]
                position = child_joint.mimic.calculate_position(mimicked_joint_position)
                transformation = parent_transformation * child_joint.calculate_transformation(position)
            else:
                transformation = parent_transformation
            transformations.update({child_joint.name: transformation})
            # call function on child
            transformations.update(self.compute_transformations(joint_state, child_joint.child_link, transformation))

        return transformations

    def transformed_frames(self, joint_state):
        """Returns the transformed frames based on the joint_state.

        Parameters
        ----------
        joint_state : :class:`~compas.robots.Configuration` | dict[str, float]
            A configuration instance or a dictionary with joint names and joint values in radians and
            meters (depending on the joint type).

        Returns
        -------
        list[:class:`Frame`]

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> config = robot.zero_configuration()
        >>> config['shoulder_pan_joint'] = 1.2
        >>> config['wrist_2_joint'] = 0.5
        >>> ft = robot.transformed_frames(config)
        >>> ft[1]
        Frame(Point(0.000, 0.000, 0.089), Vector(0.362, 0.932, 0.000), Vector(-0.932, 0.362, 0.000))

        """
        transformations = self.compute_transformations(joint_state)
        return [j.current_origin.transformed(transformations[j.name]) for j in self.iter_joints()]

    def transformed_axes(self, joint_state):
        """Returns the transformed axes based on the joint_state.

        Parameters
        ----------
        joint_state : :class:`~compas.robots.Configuration` | dict[str, float]
            A configuration instance or a dictionary with joint names and joint values in radians and
            meters (depending on the joint type).

        Returns
        -------
        list[:class:`Vector`]

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> config = robot.zero_configuration()
        >>> config['shoulder_pan_joint'] = 1.2
        >>> config['wrist_2_joint'] = 0.5
        >>> at = robot.transformed_axes(config)
        >>> at[3]
        Vector(-0.932, 0.362, 0.000)

        """
        transformations = self.compute_transformations(joint_state)
        return [j.current_axis.transformed(transformations[j.name]) for j in self.iter_joints() if j.current_axis.vector.length]

    def forward_kinematics(self, joint_state, link_name=None):
        """Calculate the robot's forward kinematic.

        Parameters
        ----------
        joint_state : :class:`~compas.robots.Configuration` | dict[str, float]
            A configuration instance or a dictionary with joint names and joint values in radians and
            meters (depending on the joint type).
        link_name : str, optional
            The name of the link we want to calculate the forward kinematics for.
            Defaults to the end-effector link name.

        Returns
        -------
        :class:`Frame`
            The frame at the end-effector link in the world coordinate system.

        Examples
        --------
        >>> robot = RobotModel.ur5()
        >>> config = robot.zero_configuration()
        >>> robot.forward_kinematics(config)
        Frame(Point(0.817, 0.191, -0.005), Vector(-0.000, 1.000, 0.000), Vector(1.000, 0.000, 0.000))

        """
        if link_name is None:
            ee_link = self.get_end_effector_link()
        else:
            ee_link = self.get_link_by_name(link_name)
        joint = ee_link.parent_joint
        if joint:
            transformations = self.compute_transformations(joint_state)
            return joint.current_origin.transformed(transformations[joint.name])
        else:
            return Frame.worldXY()  # if we ask forward from base link

    @staticmethod
    def _consolidate_meshes(meshes, key, **kwargs):
        meshes = meshes or []
        mesh = kwargs.get(key)
        if mesh:
            meshes.append(mesh)
            del kwargs[key]
        return meshes, kwargs

    def _check_link_name(self, name):
        all_link_names = [l.name for l in self.links]  # noqa: E741
        if name in all_link_names:
            raise ValueError("Link name '%s' already used in chain." % name)

    def add_link(self, name, visual_meshes=None, visual_color=None, collision_meshes=None, **kwargs):
        """Adds a link to the robot model.

        Provides an easy way to programmatically add a link to the robot model.

        Parameters
        ----------
        name : str
            The name of the link
        visual_meshes : list[:class:`~compas.datastructures.Mesh` | :class:`~compas.geometry.Shape`], optional
            The link's visual mesh.
        visual_color : [float, float, float], optional
            The rgb color of the mesh.
            Defaults to (0.8, 0.8, 0.8)
        collision_meshes : list[:class:`~compas.datastructures.Mesh`], optional
            The link's collision mesh.
        **kwargs : dict[str, Any], optional
            The keyword arguments (kwargs) collected in a dict.
            These allow using non-standard attributes absent in the URDF specification.

        Returns
        -------
        :class:`Link`
            The created `Link`

        Raises
        ------
        ValueError
            If the link name is already used in the chain.

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> from compas.geometry import Sphere
        >>> sphere = Sphere((0, 0, 0), 1)
        >>> mesh = Mesh.from_shape(sphere)
        >>> robot = RobotModel('robot')
        >>> link = robot.add_link('link0', visual_mesh=mesh)

        """
        self._check_link_name(name)
        visual_meshes, kwargs = self._consolidate_meshes(visual_meshes, 'visual_mesh', **kwargs)
        collision_meshes, kwargs = self._consolidate_meshes(collision_meshes, 'collision_mesh', **kwargs)
        if not visual_color:
            visual_color = (0.8, 0.8, 0.8)

        visuals = []
        collisions = []

        for visual in visual_meshes:
            if isinstance(visual, Mesh):
                v = Visual(Geometry(MeshDescriptor("")))
                v.geometry.shape.meshes = [visual]
            else:
                v = Visual.from_primitive(visual)
            v.material = Material(color=Color("%f %f %f 1" % visual_color))
            visuals.append(v)

        for collision in collision_meshes:  # use visual_mesh as collision_mesh if none passed?
            if isinstance(collision, Mesh):
                c = Collision(Geometry(MeshDescriptor("")))
                c.geometry.shape.meshes = [collision]
            else:
                c = Collision.from_primitive(collision)
            collisions.append(c)

        link = Link(name, visual=visuals, collision=collisions, **kwargs)
        self.links.append(link)
        # Must build the tree structure, if adding the first link to an empty robot
        if len(self.links) == 1:
            self._rebuild_tree()
            self._create(self.root, Transformation())
        return link

    def remove_link(self, name):
        """Removes a link to the robot model.

        Provides an easy way to programmatically remove a link from the robot model.

        Parameters
        ----------
        name : str
            The name of the link

        """
        self.links = [link for link in self.links if link.name != name]

    def add_joint(self, name, type, parent_link, child_link, origin=None, axis=None, limit=None, **kwargs):
        """Adds a joint to the robot model.

        Provides an easy way to programmatically add a joint to the robot model.

        Parameters
        ----------
        name : str
            The name of the joint
        type : int
            The joint type, e.g. Joint.REVOLUTE
        parent_link : :class:`Link`
            The joint's parent link.
        child_link : :class:`Link`
            The joint's child link.
        origin : :class:`~compas.geometry.Frame`
            The joint's origin frame.
        axis : :class:`~compas.geometry.Vector`
            The joint's axis.
        limit : list of 2 float
            The lower and upper limits of the joint (used for joint types Joint.REVOLUTE or Joint.PRISMATIC)
        **kwargs : dict[str, Any], optional
            The keyword arguments (kwargs) collected in a dict.
            These allow using non-standard attributes absent in the URDF specification.

        Returns
        -------
        :class:`Joint`
            The created `Joint`

        Raises
        ------
        ValueError
            If the joint name is already used in the chain.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> robot = RobotModel('robot')
        >>> parent_link = robot.add_link('link0')
        >>> child_link = robot.add_link('link1')
        >>> origin = Frame.worldXY()
        >>> axis = (1, 0, 0)
        >>> j = robot.add_joint("joint1", Joint.CONTINUOUS, parent_link, child_link, origin, axis)

        """
        all_joint_names = [j.name for j in self.joints]
        if name in all_joint_names:
            raise ValueError("Joint name '%s' already used in chain." % name)

        if origin:
            origin = Frame(origin.point, origin.xaxis, origin.yaxis)
        if axis:
            axis = Axis('{} {} {}'.format(*list(axis)))
        if limit:
            lower, upper = limit
            limit = Limit(lower=lower, upper=upper)

        type_str = Joint.SUPPORTED_TYPES[type]

        joint = Joint(name, type_str, parent_link.name, child_link.name, origin=origin, axis=axis, limit=limit, **kwargs)

        self.joints.append(joint)

        # Using only part of self._rebuild_tree()
        parent_link.joints.append(joint)
        child_link.parent_joint = joint

        self._links[parent_link.name] = parent_link
        self._adjacency[parent_link.name] = [joint.name for joint in parent_link.joints]
        self._links[child_link.name] = child_link

        if not parent_link.parent_joint:
            self.root = parent_link

        joint.child_link = child_link
        self._joints[joint.name] = joint
        self._adjacency[joint.name] = [child_link.name]

        self._create(self.root, Transformation())

        return joint

    def remove_joint(self, name):
        """Removes a joint to the robot model.

        Provides an easy way to programmatically remove a joint from the robot model.

        Parameters
        ----------
        name : str
            The name of the joint

        Returns
        -------
        None

        """
        joint = self.get_joint_by_name(name)
        self.joints = [j for j in self.joints if j.name != name]
        parent_link = self.get_link_by_name(joint.parent.link)
        parent_link.joints = [j for j in parent_link.joints if j.name != name]
        self._adjacency[parent_link.name] = [j.name for j in parent_link.joints]
        del self._links[joint.child.link]
        del self._joints[name]
        del self._adjacency[name]


URDFParser.install_parser(RobotModel, 'robot')
URDFParser.install_parser(Material, 'robot/material')
URDFParser.install_parser(Color, 'robot/material/color')
URDFParser.install_parser(Texture, 'robot/material/texture')
