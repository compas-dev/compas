from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools

from compas.files import URDF
from compas.files import URDFParser
from compas.geometry import Frame
from compas.geometry import Transformation
from compas.topology import shortest_path

from compas.robots.model.geometry import Color
from compas.robots.model.geometry import Material
from compas.robots.model.geometry import Texture
from compas.robots.model.joint import Joint
from compas.robots.resources import DefaultMeshLoader


__all__ = ['RobotModel']


class RobotModel(object):
    """RobotModel is the root element of the model.

    Instances of this class represent an entire robot as defined in an URDF
    structure.

    In line with URDF limitations, only tree structures can be represented by
    this model, ruling out all parallel robots.

    Attributes:
        name: Unique name of the robot.
        joints: List of joint elements.
        links: List of links of the robot.
        materials: List of global materials.
        root: Root link of the model.
        attr: Non-standard attributes.
    """

    def __init__(self, name, joints=[], links=[], materials=[], **kwargs):
        self.name = name
        self.joints = joints
        self.links = links
        self.materials = materials
        self.attr = kwargs
        self.root = None
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

        Args:
            file: file name or file object.

        Returns:
            A robot model instance.
        """
        urdf = URDF.from_file(file)
        return urdf.robot

    @classmethod
    def from_urdf_string(cls, text):
        """Construct a robot model from a URDF description as string.

        Args:
            text: string containing the XML URDF model.

        Returns:
            A robot model instance.
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
        """
        for joint in self.joints:
            if str(joint.child) == link.name:
                return joint
        return None

    def get_link_by_name(self, name):
        """Get a link in a robot model matching by its name.

        Args:
            name: link name.

        Returns:
            A link instance.
        """
        return self._links.get(name, None)

    def get_joint_by_name(self, name):
        """Get a joint in a robot model matching by its name.

        Args:
            name: joint name.

        Returns:
            A joint instance.
        """
        return self._joints.get(name, None)

    def iter_links(self):
        """Iterator over the links that starts with the root link.

        Returns:
            Iterator of all links starting at root.
        """

        def func(cjoints, links):
            for j in cjoints:
                link = j.child_link
                links.append(link)
                links += func(link.joints, [])
            return links

        return iter(func(self.root.joints, [self.root]))

    def iter_joints(self):
        """Iterator over the joints that starts with the root link's
            children joints.

        Returns:
            Iterator of all joints starting at root.
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

        Args:
            link_start_name: Name of the starting link of the chain,
                or ``None`` to start at root.
            link_end_name: Name of the final link of the chain,
                or ``None`` to try to identify the last link.

        Returns:
            Iterator of the chain of links.

        .. note::
            This method differs from :meth:`iter_links` in that it returns the chain respecting
            the tree structure, hence if one link branches into two or more joints, only the
            branch matching the end link will be returned.
        """
        chain = self.iter_chain(link_start_name, link_end_name)
        for link in map(self.get_link_by_name, chain):
            # If None, it's not a link
            if link:
                yield link

    def iter_joint_chain(self, link_start_name=None, link_end_name=None):
        """Iterator over the chain of joints between a pair of start and end links.

        Args:
            link_start_name: Name of the starting link of the chain,
                or ``None`` to start at root.
            link_end_name: Name of the final link of the chain,
                or ``None`` to try to identify the last link.

        Returns:
            Iterator of the chain of joints.

        .. note::
            This method differs from :meth:`iter_joints` in that it returns the
            chain respecting the tree structure, hence if one link branches into
            two or more joints, only the branch matching the end link will be
            returned.
        """
        chain = self.iter_chain(link_start_name, link_end_name)
        for joint in map(self.get_joint_by_name, chain):
            # If None, it's not a joint
            if joint:
                yield joint

    def iter_chain(self, start=None, end=None):
        """Iterator over the chain of all elements between a pair of start and end elements.

        Args:
            start: Name of the starting element of the chain,
                or ``None`` to start at the root link.
            end: Name of the final element of the chain,
                or ``None`` to try to identify the last element.

        Returns:
            Iterator of the chain of links and joints.
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
        joints = self.iter_joints()
        return [joint for joint in joints if joint.is_configurable()]

    def get_joint_types(self):
        joints = self.get_configurable_joints()
        return [joint.type for joint in joints]

    def get_positions(self):
        joints = self.get_configurable_joints()
        return [j.position for j in joints]

    def get_configurable_joint_names(self):
        joints = self.get_configurable_joints()
        return [j.name for j in joints]

    def get_end_effector_link_name(self):
        joints = self.get_configurable_joints()
        clink = joints[-1].child_link
        for j in clink.joints:
            if j.type == Joint.FIXED:
                return j.child
        return clink.name

    def get_base_link_name(self):
        joints = self.get_configurable_joints()
        return joints[0].parent.link

    def load_geometry(self, *resource_loaders, **kwargs):
        """Load external geometry resources, such as meshes.

        Args:
            resource_loaders: List of objects that implement the
                resource loading interface (:class:`compas.robots.AbstractMeshLoader`)
                and can retrieve external geometry.
            force: True if it should force reloading even if the geometry
                has been loaded already, otherwise False.
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

        Returns:
            list: List of :class:`compas.geometry.Frame` of all links with a visual representation.
        """
        frames = []
        for link in self.iter_links():
            if len(link.visual) and link.parent_joint:
                frames.append(link.parent_joint.origin.copy())
        return frames

    @property
    def axes(self):
        """Returns the joints' axes.

        Returns:
            list: Axis vectors of all joints.
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

URDFParser.install_parser(RobotModel, 'robot')
URDFParser.install_parser(Material, 'robot/material')
URDFParser.install_parser(Color, 'robot/material/color')
URDFParser.install_parser(Texture, 'robot/material/texture')
