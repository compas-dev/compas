from __future__ import absolute_import, division, print_function

from compas.files import URDF

from .geometry import Box, Capsule, colour, Cylinder, Geometry, Material, MeshDescriptor, Origin, Sphere, Texture

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
URDF.add_parser(colour, 'robot/link/visual/material/colour')
URDF.add_parser(Texture, 'robot/link/visual/material/texture')
