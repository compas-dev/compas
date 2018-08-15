from __future__ import absolute_import, division, print_function

from compas.files import URDF

from .geometry import SCALE_FACTOR, colour, Material, Texture

__all__ = ['Robot']


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
URDF.add_parser(Material, 'robot/material')
URDF.add_parser(colour, 'robot/material/colour')
URDF.add_parser(Texture, 'robot/material/texture')
