from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.files import URDF
from compas.topology import shortest_path

from .geometry import SCALE_FACTOR
from .geometry import Color
from .geometry import Material
from .geometry import Texture

__all__ = ['Robot']


class Robot(object):
    """Robot is the root element of the model.

    Instances of this class represent an entire robot as defined in an URDF structure.

    In line with URDF limitations, only tree structures can be represented by this
    model, ruling out all parallel robots.

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

    def get_frames(self):
        """Get the frames of links that have a visual node.

        Returns:
            list: List of :class:`compas.geometry.Frame` of all links with a visual representation.
        """
        frames = []
        for link in self.iter_links():
            if len(link.visual):
                frames.append(link.parent_joint.origin.copy())
        return frames

    def get_axes(self):
        """Get axes of all joints.

        Returns:
            list: Axis vectors of all joints.
        """
        axes = []
        for joint in self.iter_joints():
            if joint.axis:
                axes.append(joint.axis.vector)
        return axes

    def draw_visual(self):
        visual = []
        for link in self.iter_links():
            for item in link.visual:
                visual.append(item.draw())
        return visual

    def draw_collision(self):
        collision = []
        for link in self.iter_links():
            for item in link.collision:
                collision.append(item.draw())
        return collision

    def draw(self):
        return self.draw_visual()


URDF.add_parser(Robot, 'robot')
URDF.add_parser(Material, 'robot/material')
URDF.add_parser(Color, 'robot/material/color')
URDF.add_parser(Texture, 'robot/material/texture')
