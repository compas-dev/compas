from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import json

from compas.base import Base
from compas.files import URDF
from compas.files import URDFParser
from compas.files import URDFElement
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.robots.model.geometry import Color
from compas.robots.model.geometry import Geometry
from compas.robots.model.geometry import Material
from compas.robots.model.geometry import MeshDescriptor
from compas.robots.model.geometry import Origin
from compas.robots.model.geometry import Texture
from compas.robots.model.geometry import _attr_to_data
from compas.robots.model.geometry import _attr_from_data
from compas.robots.model.joint import Axis
from compas.robots.model.joint import Joint
from compas.robots.model.joint import Limit
from compas.robots.model.link import Collision
from compas.robots.model.link import Link
from compas.robots.model.link import Visual
from compas.robots.resources import DefaultMeshLoader
from compas.topology import shortest_path


__all__ = ['RobotModel']


class RobotModel(Base):
    """RobotModel is the root element of the model.

    Instances of this class represent an entire robot as defined in an URDF
    structure.

    In line with URDF limitations, only tree structures can be represented by
    this model, ruling out all parallel robots.

    Attributes
    ----------
    name:
        Unique name of the robot.
    joints:
        List of joint elements.
    links:
        List of links of the robot.
    materials:
        List of global materials.
    root:
        Root link of the model.
    attr:
        Non-standard attributes.
    """

    def __init__(self, name, joints=[], links=[], materials=[], **kwargs):
        super(RobotModel, self).__init__()
        self.name = name
        self.joints = list(joints)
        self.links = list(links)
        self.materials = list(materials)
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

    def to_data(self):
        """Returns the data dictionary that represents the :class:`RobotModel`.
        To be used in conjunction with :meth:`compas.robot.RobotModel.from_data()`.

        Returns
        -------
        dict
            The RobotModel's data.
        """
        return self.data

    @classmethod
    def from_data(cls, data):
        """Construct the :class:`compas.robots.RobotModel` from its data representation.
        To be used in conjunction with :meth:`compas.robot.RobotModel.to_data()`.
        """
        robot_model = cls(data['name'])
        robot_model.data = data
        return robot_model

    def to_json(self, filepath):
        with open(filepath, 'w+') as f:
            json.dump(self.data, f)

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        return cls.from_data(data)

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
        file:
            file name or file object.

        Returns
        -------
        A robot model instance.

        Examples
        --------
        >>> model = RobotModel.from_urdf_file(ur5_urdf_file)
        >>> print(model)
        Robot name=ur5, Links=11, Joints=10 (6 configurable)
        """
        urdf = URDF.from_file(file)
        return urdf.robot

    def to_urdf_file(self, file, prettify=False):
        """Construct a URDF file model description from a robot model.

        Parameters
        ----------
        file:
            file name or file object.

        Returns
        -------
        ``None``
        """
        urdf = URDF.from_robot(self)
        urdf.to_file(file, prettify)

    @classmethod
    def from_urdf_string(cls, text):
        """Construct a robot model from a URDF description as string.

        Parameters
        ----------
        text:
            String containing the XML URDF model.

        Returns
        -------
        A robot model instance.

        Examples
        --------
        >>> urdf_string = '<?xml version="1.0" encoding="UTF-8"?><robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="panda"></robot>'
        >>> model = RobotModel.from_urdf_string(urdf_string)
        """
        urdf = URDF.from_string(text)
        return urdf.robot

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
        link : :class:`compas.robots.Link`
            The link of which we want to know the parent joint.

        Returns
        -------
        :class:`compas.robots.Joint`
            The parent joint of the link.

        Examples
        --------
        >>> j = robot.find_parent_joint(link1)
        >>> j.name
        'joint1'
        """
        for joint in self.joints:
            if str(joint.child) == link.name:
                return joint
        return None

    def get_link_by_name(self, name):
        """Get a link in a robot model matching by its name.

        Parameters
        ----------
        name:
            link name.

        Returns
        -------
        A link instance.

        Examples
        --------
        >>> l = robot.get_link_by_name('world')
        >>> l.name
        'world'
        """
        return self._links.get(name, None)

    def get_joint_by_name(self, name):
        """Get a joint in a robot model matching by its name.

        Parameters
        ----------
        name:
            joint name.

        Returns
        -------
        A joint instance.

        Examples
        --------
        >>> j = robot.get_joint_by_name('joint1')
        >>> j.name
        'joint1'
        """
        return self._joints.get(name, None)

    def iter_links(self):
        """Iterator over the links that starts with the root link.

        Returns
        -------
        Iterator of all links starting at root.

        Examples
        --------
        >>> [l.name for l in robot.iter_links()]
        ['world', 'link1', 'link2']
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
        >>> [j.name for j in robot.iter_joints()]
        ['joint1', 'joint2']
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
        link_start_name: str or ``None``
            Name of the starting link of the chain. Defaults to the root link name.
        link_end_name: str or ``None``
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
        >>> [l.name for l in robot.iter_link_chain('world', 'link2')]
        ['world', 'link1', 'link2']
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
        link_start_name: str or ``None``
            Name of the starting link of the chain. Defaults to the root link name.
        link_end_name: str or ``None``
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
        >>> [j.name for j in robot.iter_joint_chain('world', 'link2')]
        ['joint1', 'joint2']
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
        start: str or ``None``
            Name of the starting element of the chain. Defaults to the root link name.
        end: str or ``None``
            Name of the final element of the chain. Defaults to the name of the last element.

        Returns
        -------
        Iterator of the chain of links and joints (names).

        Examples
        --------
        >>> list(robot.iter_chain('world', 'link2'))
        ['world', 'joint1', 'link1', 'joint2', 'link2']
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

        Returns
        -------
        list of :class: `compas.robots.Joint`

        Examples
        --------
        >>> joints = robot.get_configurable_joints()
        >>> [j.name for j in joints]
        ['joint1', 'joint2']
        """
        joints = self.iter_joints()
        return [joint for joint in joints if joint.is_configurable()]

    def get_joint_types(self):
        """Returns the joint types of the configurable joints.

        Returns
        -------
        list of int

        Examples
        --------
        >>> robot.get_joint_types() == [Joint.CONTINUOUS, Joint.CONTINUOUS]
        True
        """
        joints = self.get_configurable_joints()
        return [joint.type for joint in joints]

    def get_configurable_joint_names(self):
        """Returns the configurable joint names.

        Returns
        -------
        list of str

        Examples
        --------
        >>> robot.get_configurable_joint_names()
        ['joint1', 'joint2']
        """
        joints = self.get_configurable_joints()
        return [j.name for j in joints]

    def get_end_effector_link(self):
        """Returns the end effector link.

        Returns
        -------
        :class:`compas.robots.Link`

        Examples
        --------
        >>> ee_link = robot.get_end_effector_link()
        >>> ee_link.name
        'link2'
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

        Examples
        --------
        >>> robot.get_end_effector_link_name()
        'link2'
        """
        link = self.get_end_effector_link()
        return link.name

    def get_base_link_name(self):
        """Returns the name of the base link.

        Returns
        -------
        str

        Examples
        --------
        >>> robot.get_base_link_name()
        'world'
        """
        joints = self.get_configurable_joints()
        return joints[0].parent.link

    def load_geometry(self, *resource_loaders, **kwargs):
        """Load external geometry resources, such as meshes.

        Parameters
        ----------
        resource_loaders: :class:`compas.robots.AbstractMeshLoader`
            List of objects that implement the
            resource loading interface (:class:`compas.robots.AbstractMeshLoader`)
            and can retrieve external geometry.
        force: boolean
            True if it should force reloading even if the geometry
            has been loaded already, otherwise False.


        Examples
        --------
        >>> loader = GithubPackageMeshLoader('ros-industrial/abb', 'abb_irb6600_support', 'kinetic-devel')
        >>> urdf = loader.load_urdf('irb6640.urdf')
        >>> model = RobotModel.from_urdf_file(urdf)
        >>> model.load_geometry(loader)
        """
        force = kwargs.get('force', False)

        loaders = list(resource_loaders)
        loaders.insert(0, DefaultMeshLoader())

        for link in self.links:
            for element in itertools.chain(link.collision, link.visual):
                shape = element.geometry.shape
                needs_reload = force or not shape.geometry
                if 'filename' in dir(shape) and needs_reload:
                    for loader in loaders:
                        if loader.can_load_mesh(shape.filename):
                            shape.geometry = loader.load_mesh(shape.filename)
                            break

                    if not shape.geometry:
                        raise Exception('Unable to load geometry for {}'.format(shape.filename))

    @property
    def frames(self):
        """Returns the frames of links that have a visual node.

        Returns
        -------
        list
            List of :class:`compas.geometry.Frame` of all links with a visual representation.
        """
        frames = []
        for link in self.iter_links():
            if len(link.visual) and link.parent_joint:
                frames.append(link.parent_joint.origin.copy())
        return frames

    @property
    def axes(self):
        """Returns the joints' axes.

        Returns
        -------
        list
            Axis vectors of all joints.
        """
        axes = []
        for joint in self.iter_joints():
            if joint.axis:
                axes.append(joint.axis.vector)
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
        """Private function called during initialisation to transform origins and axes.

        Parameters
        ----------
        link : :class:`compas.robots.Link`
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

        Returns
        -------
        None

        Examples
        --------
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
        joint_state : dict
            A dictionary with the joint names as keys and values in radians and
            meters (depending on the joint type).
        link : :class:`compas.robots.Link`
            Link instance to calculate the child joint's transformation.
        parent_transformation : :class:`Transformation`
            The transfomation of the parent joint.

        Returns
        -------
        dict of str: :class:`Transformation`
            A dictionary with the joint names as keys and values are the joint's respective transformation.

        Examples
        --------
        >>> names = robot.get_configurable_joint_names()
        >>> values = [-2.238, -1.153, -2.174, 0.185, 0.667, 0.000]
        >>> joint_state = dict(zip(names, values))
        >>> transformations = robot.compute_transformations(joint_state)
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
        joint_state : dict
            A dictionary with the joint names as keys and values in radians and
            meters (depending on the joint type).

        Returns
        -------
        list of :class:`Frame`

        Examples
        --------
        >>> joint_names = robot.get_configurable_joint_names()
        >>> values = [1.2, 0.5]
        >>> joint_state = dict(zip(joint_names, values))
        >>> frames_transformed = robot.transformed_frames(joint_state)
        >>> frames_transformed[0]
        Frame(Point(0.000, 0.000, 0.000), Vector(0.362, 0.932, 0.000), Vector(-0.932, 0.362, 0.000))
        """
        transformations = self.compute_transformations(joint_state)
        return [j.origin.transformed(transformations[j.name]) for j in self.iter_joints()]

    def transformed_axes(self, joint_state):
        """Returns the transformed axes based on the joint_state.

        Parameters
        ----------
        joint_state : dict
            A dictionary with the joint names as keys and values in radians and
            meters (depending on the joint type).

        Returns
        -------
        list of :class:`Vector`

        Examples
        --------
        >>> joint_names = robot.get_configurable_joint_names()
        >>> values = [1.2, 0.5]
        >>> joint_state = dict(zip(joint_names, values))
        >>> robot.transformed_axes(joint_state)
        [Vector(0.000, 0.000, 1.000), Vector(0.000, 0.000, 1.000)]
        """
        transformations = self.compute_transformations(joint_state)
        return [j.axis.transformed(transformations[j.name]) for j in self.iter_joints() if j.axis.vector.length]

    def forward_kinematics(self, joint_state, link_name=None):
        """Calculate the robot's forward kinematic.

        Parameters
        ----------
        joint_state : dict
            A dictionary with the joint names as keys and values in radians and
            meters (depending on the joint type).
        link_name : str, optional
            The name of the link we want to calculate the forward kinematics for.
            Defaults to the end-effector link name.

        Returns
        -------
        :class:`Frame`
            The (ee) link's frame in the world coordinate system.

        Examples
        --------
        >>> names = robot.get_configurable_joint_names()
        >>> values = [-2.238, -1.153, -2.174, 0.185, 0.667, 0.000]
        >>> joint_state = dict(zip(names, values))
        >>> frame_WCF = robot.forward_kinematics(joint_state)
        """
        if link_name is None:
            ee_link = self.get_end_effector_link()
        else:
            ee_link = self.get_link_by_name(link_name)
        joint = ee_link.parent_joint
        if joint:
            transformations = self.compute_transformations(joint_state)
            return joint.origin.transformed(transformations[joint.name])
        else:
            return Frame.worldXY()  # if we ask forward from base link

    @staticmethod
    def _consolidate_meshes(meshes, key, **kwargs):
        meshes = meshes or []
        mesh = kwargs.get(key)
        if mesh:
            meshes.append(mesh)
        return meshes

    def add_link(self, name, visual_meshes=None, visual_color=None, collision_meshes=None, **kwargs):
        """Adds a link to the robot model.

        Provides an easy way to programmatically add a link to the robot model.

        Parameters
        ----------
        name : str
            The name of the link
        visual_meshes : list of :class:`compas.datastructures.Mesh`, optional
            The link's visual mesh.
        visual_color : list of 3 float, optional
            The rgb color of the mesh. Defaults to (0.8, 0.8, 0.8)
        collision_meshes : list of :class:`compas.datastructures.Mesh`, optional
            The link's collision mesh.

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
        >>> sphere = Sphere((0, 0, 0), 1)
        >>> mesh = Mesh.from_shape(sphere)
        >>> robot = RobotModel('robot')
        >>> link = robot.add_link('link0', visual_mesh=mesh)
        """
        visual_meshes = self._consolidate_meshes(visual_meshes, 'visual_mesh', **kwargs)
        collision_meshes = self._consolidate_meshes(collision_meshes, 'collision_mesh', **kwargs)

        all_link_names = [l.name for l in self.links]  # noqa: E741
        if name in all_link_names:
            raise ValueError("Link name '%s' already used in chain." % name)

        visual = []
        collision = []

        for visual_mesh in visual_meshes:
            if not visual_color:
                visual_color = (0.8, 0.8, 0.8)
            v = Visual(Geometry(MeshDescriptor("")))
            v.material = Material(color=Color("%f %f %f 1" % visual_color))
            v.geometry.shape.geometry = visual_mesh
            visual.append(v)

        for collision_mesh in collision_meshes:  # use visual_mesh as collision_mesh if none passed?
            c = Collision(Geometry(MeshDescriptor("")))
            c.geometry.shape.geometry = collision_mesh
            collision.append(c)

        link = Link(name, visual=visual, collision=collision, **kwargs)
        self.links.append(link)
        return link

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
        origin : :class:`compas.geometry.Frame`
            The joint's origin frame.
        axis : :class:`compas.geometry.Vector`
            The joint's axis.
        limit : list of 2 float
            The lower and upper limits of the joint (used for joint types Joint.REVOLUTE or Joint.PRISMATIC)

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
            origin = Origin(origin.point, origin.xaxis, origin.yaxis)
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

        # Using only part of self._create(link, parent_transformation)
        parent_transformation = Transformation()
        for item in itertools.chain(parent_link.visual, parent_link.collision):
            if not item.init_transformation:
                item.init_transformation = parent_transformation
            else:
                parent_transformation = item.init_transformation

        joint._create(parent_transformation)

        for item in itertools.chain(child_link.visual, child_link.collision):
            item.init_transformation = joint.current_transformation

        return joint


URDFParser.install_parser(RobotModel, 'robot')
URDFParser.install_parser(Material, 'robot/material')
URDFParser.install_parser(Color, 'robot/material/color')
URDFParser.install_parser(Texture, 'robot/material/texture')


if __name__ == '__main__':
    import os
    import doctest
    from compas import HERE
    from compas.geometry import Sphere  # noqa: F401
    from compas.robots import GithubPackageMeshLoader  # noqa: F401

    ur5_urdf_file = os.path.join(HERE, '..', '..', 'tests', 'compas', 'robots', 'fixtures', 'ur5.xacro')

    robot = RobotModel("robot", links=[], joints=[])
    link0 = robot.add_link("world")
    link1 = robot.add_link("link1")
    link2 = robot.add_link("link2")
    robot.add_joint("joint1", Joint.CONTINUOUS, link0, link1, Frame.worldXY(), (0, 0, 1))
    robot.add_joint("joint2", Joint.CONTINUOUS, link1, link2, Frame.worldXY(), (0, 0, 1))
    doctest.testmod(globs=globals())
