from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas.files import URDF
from compas.geometry import Frame
from compas.geometry.xforms import Transformation

from .geometry import Box
from .geometry import Capsule
from .geometry import Color
from .geometry import Cylinder
from .geometry import Geometry
from .geometry import Material
from .geometry import MeshDescriptor
from .geometry import Origin
from .geometry import Sphere
from .geometry import Texture

__all__ = ['Link', 'Inertial', 'Visual', 'Collision', 'Mass', 'Inertia']


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

    def draw(self):
        return self.geometry.draw()

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

    def draw(self):
        return self.geometry.draw()


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
        parent_joint: The reference to a parent joint if it exists
    """

    def __init__(self, name, type=None, visual=[], collision=[], inertial=None, **kwargs):
        self.name = name
        self.type = type
        self.visual = visual
        self.collision = collision
        self.inertial = inertial
        self.attr = kwargs
        self.joints = []
        self.parent_joint = None

    def create(self, urdf_importer, meshcls, parent_origin):
        """Recursive function to create all geometry shapes.
        """
        for item in self.visual:
            item.geometry.shape.create(urdf_importer, meshcls)
        for item in self.collision:
            item.geometry.shape.create(urdf_importer, meshcls)

        transformation = Transformation.from_frame(parent_origin)

        # former DAE files have yaxis and zaxis swapped
        # TODO: already fix in conversion to obj or in import
        # TODO: move to mesh importer!
        fx = Frame(parent_origin.point, parent_origin.xaxis, parent_origin.zaxis)
        transformation_dae = Transformation.from_frame(fx)

        for item in self.visual:
            if type(item.geometry.shape) == MeshDescriptor:
                if os.path.splitext(item.geometry.shape.filename)[1] == ".dae":
                    item.geometry.shape.transform(transformation_dae)
                else:
                    item.geometry.shape.transform(transformation)
            else:
                item.geometry.shape.transform(transformation)

        for item in self.collision:
            if type(item.geometry.shape) == MeshDescriptor:
                if os.path.splitext(item.geometry.shape.filename)[1] == ".dae":
                    item.geometry.shape.transform(transformation_dae)
                else:
                    item.geometry.shape.transform(transformation)
            else:
                item.geometry.shape.transform(transformation)

        for cjoint in self.joints:
            cjoint.origin.create(transformation)
            if cjoint.axis:
                cjoint.axis.create(transformation)
            clink = cjoint.child_link
            clink.create(urdf_importer, meshcls, cjoint.origin)

    def update(self, joint_state, parent_transformation, reset_transformation):
        """Recursive function to apply the transformations given by the joint
            state.

        Joint_states are given absolute, so it is necessary to reset the current
        transformation.
        """
        relative_transformation = parent_transformation * reset_transformation

        for item in self.visual:
            item.geometry.shape.transform(relative_transformation)
        for item in self.collision:
            item.geometry.shape.transform(relative_transformation)

        for joint in self.joints:
            # 1. Get reset transformation
            reset_transformation = joint.calculate_reset_transformation()
            # 2. Reset
            joint.reset_transform()
            #joint.transform(reset_transformation) # why does this not work properly....

            # 3. Calculate transformation
            if joint.name in joint_state.keys():
                position = joint_state[joint.name]
                transformation = joint.calculate_transformation(position)
                transformation = parent_transformation * transformation
                joint.position = position
            else:
                transformation = parent_transformation

            # 4. Apply on joint
            joint.transform(transformation)
            # 4. Apply function to all children
            joint.child_link.update(joint_state, transformation, reset_transformation)



URDF.add_parser(Link, 'robot/link')
URDF.add_parser(Inertial, 'robot/link/inertial')
URDF.add_parser(Mass, 'robot/link/inertial/mass')
URDF.add_parser(Inertia, 'robot/link/inertial/inertia')

URDF.add_parser(Visual, 'robot/link/visual')
URDF.add_parser(Collision, 'robot/link/collision')

URDF.add_parser(Origin, 'robot/link/inertial/origin', 'robot/link/visual/origin', 'robot/link/collision/origin')
URDF.add_parser(Geometry, 'robot/link/visual/geometry', 'robot/link/collision/geometry')
URDF.add_parser(MeshDescriptor, 'robot/link/visual/geometry/mesh', 'robot/link/collision/geometry/mesh')
URDF.add_parser(Box, 'robot/link/visual/geometry/box', 'robot/link/collision/geometry/box')
URDF.add_parser(Cylinder, 'robot/link/visual/geometry/cylinder', 'robot/link/collision/geometry/cylinder')
URDF.add_parser(Sphere, 'robot/link/visual/geometry/sphere', 'robot/link/collision/geometry/sphere')
URDF.add_parser(Capsule, 'robot/link/visual/geometry/capsule', 'robot/link/collision/geometry/capsule')

URDF.add_parser(Material, 'robot/link/visual/material')
URDF.add_parser(Color, 'robot/link/visual/material/color')
URDF.add_parser(Texture, 'robot/link/visual/material/texture')
