from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data
from compas.files import URDFElement
from compas.files import URDFParser
from compas.geometry import Box
from compas.geometry import Capsule
from compas.geometry import Cylinder
from compas.geometry import Frame
from compas.geometry import Sphere
from compas.geometry import Transformation

from .base import FrameProxy
from .base import _attr_from_data
from .base import _attr_to_data

from .geometry import BoxProxy
from .geometry import CapsuleProxy
from .geometry import Color
from .geometry import CylinderProxy
from .geometry import Geometry
from .geometry import Material
from .geometry import MeshDescriptor
from .geometry import SphereProxy
from .geometry import Texture


class Mass(Data):
    """Represents a value of mass usually related to a link."""

    def __init__(self, value):
        super(Mass, self).__init__()
        self.value = float(value)

    def __str__(self):
        return str(self.value)

    def get_urdf_element(self):
        attributes = {"value": self.value}
        return URDFElement("mass", attributes)

    @property
    def data(self):
        return {"value": self.value}

    @data.setter
    def data(self, data):
        self.value = data["value"]

    @classmethod
    def from_data(cls, data):
        return cls(**data)


class Inertia(Data):
    """Rotational inertia matrix (3x3) represented in the inertia frame.

    Since the rotational inertia matrix is symmetric, only 6 above-diagonal
    elements of this matrix are specified here, using the attributes
    ``ixx``, ``ixy``, ``ixz``, ``iyy``, ``iyz``, ``izz``.

    """

    def __init__(self, ixx=0.0, ixy=0.0, ixz=0.0, iyy=0.0, iyz=0.0, izz=0.0):
        super(Inertia, self).__init__()
        self.ixx = float(ixx)
        self.ixy = float(ixy)
        self.ixz = float(ixz)
        self.iyy = float(iyy)
        self.iyz = float(iyz)
        self.izz = float(izz)

    def get_urdf_element(self):
        attributes = {
            "ixx": self.ixx,
            "ixy": self.ixy,
            "ixz": self.ixz,
            "iyy": self.iyy,
            "iyz": self.iyz,
            "izz": self.izz,
        }
        return URDFElement("inertia", attributes)

    @property
    def data(self):
        return {
            "ixx": self.ixx,
            "ixy": self.ixy,
            "ixz": self.ixz,
            "iyy": self.iyy,
            "iyz": self.iyz,
            "izz": self.izz,
        }

    @data.setter
    def data(self, data):
        self.ixx = data.get("ixx", 0.0)
        self.ixy = data.get("ixy", 0.0)
        self.ixz = data.get("ixz", 0.0)
        self.iyy = data.get("iyy", 0.0)
        self.iyz = data.get("iyz", 0.0)
        self.izz = data.get("izz", 0.0)

    @classmethod
    def from_data(cls, data):
        return cls(**data)


class Inertial(Data):
    """Inertial properties of a link.

    Attributes
    ----------
    origin
        This is the pose of the inertial reference frame,
        relative to the link reference frame.
    mass
        Mass of the link.
    inertia
        3x3 rotational inertia matrix, represented in the inertia frame.

    """

    def __init__(self, origin=None, mass=None, inertia=None):
        super(Inertial, self).__init__()
        self.origin = origin
        self.mass = mass
        self.inertia = inertia

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = FrameProxy.create_proxy(value)

    def get_urdf_element(self):
        elements = [self.origin, self.mass, self.inertia]
        return URDFElement("inertial", elements=elements)

    @property
    def data(self):
        return {
            "origin": self.origin.data if self.origin else None,
            "mass": self.mass.data if self.mass else None,
            "inertia": self.inertia.data if self.inertia else None,
        }

    @data.setter
    def data(self, data):
        self.origin = Frame.from_data(data["origin"]) if data["origin"] else None
        self.mass = Mass.from_data(data["mass"]) if data["mass"] else None
        self.inertia = Inertia.from_data(data["inertia"]) if data["inertia"] else None


class LinkItem(object):
    def __init__(self):
        self.init_transformation = None  # to store the init transformation
        self.current_transformation = None  # to store the current transformation
        self.native_geometry = None  # to store the link's CAD native geometry


class Visual(LinkItem, Data):
    """Visual description of a link.

    Attributes
    ----------
    geometry
        Shape of the visual element.
    origin
        Reference frame of the visual element with respect
        to the reference frame of the link.
    name
        Name of the visual element.
    material
        Material of the visual element.
    attr
        Non-standard attributes.

    """

    def __init__(self, geometry, origin=None, name=None, material=None, **kwargs):
        super(Visual, self).__init__()
        self.geometry = geometry
        self.origin = origin
        self.name = name
        self.material = material
        self.attr = kwargs

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = FrameProxy.create_proxy(value)

    def get_urdf_element(self):
        attributes = {}
        if self.name is not None:
            attributes["name"] = self.name
        attributes.update(self.attr)
        elements = [self.origin, self.geometry, self.material]
        return URDFElement("visual", attributes, elements)

    # Overriding the default name property, because sometimes the name really is `None`.
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def data(self):
        return {
            "geometry": self.geometry.data,
            "origin": self.origin.data if self.origin else None,
            "name": self.name,
            "material": self.material.data if self.material else None,
            "attr": _attr_to_data(self.attr),
            "init_transformation": self.init_transformation.data if self.init_transformation else None,
            "current_transformation": self.current_transformation.data if self.current_transformation else None,
        }

    @data.setter
    def data(self, data):
        self.geometry = Geometry.from_data(data["geometry"])
        self.origin = Frame.from_data(data["origin"]) if data["origin"] else None
        self.name = data["name"]
        self.material = Material.from_data(data["material"]) if data["material"] else None
        self.attr = _attr_from_data(data["attr"])
        self.init_transformation = (
            Transformation.from_data(data["init_transformation"]) if data["init_transformation"] else None
        )
        self.current_transformation = (
            Transformation.from_data(data["current_transformation"]) if data["current_transformation"] else None
        )

    @classmethod
    def from_data(cls, data):
        visual = cls(Geometry.from_data(data["geometry"]))
        visual.data = data
        return visual

    def get_color(self):
        """Get the RGBA color array assigned to the link.

        Only if the link has a material assigned.

        Returns
        -------
        list[float]
            List of 4 floats (``0.0-1.0``) indicating RGB colors and Alpha channel.

        """
        if self.material:
            return self.material.get_color()
        else:
            return None

    @classmethod
    def from_primitive(cls, primitive, **kwargs):
        """Create visual link from a primitive shape.

        Parameters
        ----------
        primitive : :class:`compas.geometry.Shape`
            A primitive shape.
        **kwargs : dict[str, Any], optional
            The keyword arguments (kwargs) collected in a dict.
            These allow using non-standard attributes absent in the URDF specification.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`
            A visual description object.
        """
        geometry = Geometry()
        geometry.shape = primitive
        return cls(geometry, **kwargs)


class Collision(LinkItem, Data):
    """Collidable description of a link.

    Attributes
    ----------
    geometry
        Shape of the collidable element.
    origin
        Reference frame of the collidable element with respect
        to the reference frame of the link.
    name
        Name of the collidable element.
    attr
        Non-standard attributes.

    """

    def __init__(self, geometry, origin=None, name=None, **kwargs):
        super(Collision, self).__init__()
        self.geometry = geometry
        self.origin = origin
        self.name = name
        self.attr = kwargs

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = FrameProxy.create_proxy(value)

    def get_urdf_element(self):
        attributes = {}
        if self.name is not None:
            attributes["name"] = self.name
        attributes.update(self.attr)
        elements = [self.origin, self.geometry]
        return URDFElement("collision", attributes, elements)

    # Overriding the default name property, because sometimes the name really is `None`.
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def data(self):
        return {
            "geometry": self.geometry.data,
            "origin": self.origin.data if self.origin else None,
            "name": self.name,
            "attr": _attr_to_data(self.attr),
            "init_transformation": self.init_transformation.data if self.init_transformation else None,
            "current_transformation": self.current_transformation.data if self.current_transformation else None,
        }

    @data.setter
    def data(self, data):
        self.geometry = Geometry.from_data(data["geometry"])
        self.origin = Frame.from_data(data["origin"]) if data["origin"] else None
        self.name = data["name"]
        self.attr = _attr_from_data(data["attr"])
        self.init_transformation = (
            Transformation.from_data(data["init_transformation"]) if data["init_transformation"] else None
        )
        self.current_transformation = (
            Transformation.from_data(data["current_transformation"]) if data["current_transformation"] else None
        )

    @classmethod
    def from_data(cls, data):
        collision = cls(Geometry.from_data(data["geometry"]))
        collision.data = data
        return collision

    @classmethod
    def from_primitive(cls, primitive, **kwargs):
        """Create collision link from a primitive shape.

        Parameters
        ----------
        primitive : :class:`compas.geometry.Shape`
            A primitive shape.
        **kwargs : dict[str, Any], optional
            The keyword arguments (kwargs) collected in a dict.
            These allow using non-standard attributes absent in the URDF specification.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`
            A collision description object.
        """
        geometry = Geometry()
        geometry.shape = primitive
        return cls(geometry, **kwargs)


class Link(Data):
    """Link represented as a rigid body with an inertia, visual, and collision features.

    Attributes
    ----------
    name
        Name of the link itself.
    type
        Link type. Undocumented in URDF, but used by PR2.
    visual
        Visual properties of the link.
    collision
        Collision properties of the link. This can be different
        from the visual properties of a link.
    inertial
        Inertial properties of the link.
    attr
        Non-standard attributes.
    joints
        A list of joints that are the link's children
    parent_joint
        The reference to a parent joint if it exists

    """

    def __init__(self, name, type=None, visual=(), collision=(), inertial=None, **kwargs):
        super(Link, self).__init__()
        self.name = name
        self.type = type
        self.visual = list(visual or [])
        self.collision = list(collision or [])
        self.inertial = inertial
        self.attr = kwargs
        self.joints = []
        self.parent_joint = None

    def get_urdf_element(self):
        attributes = {"name": self.name}
        if self.type is not None:
            attributes["type"] = self.type
        attributes.update(self.attr)
        elements = self.visual + self.collision + [self.inertial]
        return URDFElement("link", attributes, elements)

    @property
    def data(self):
        return {
            "name": self.name,
            "type": self.type,
            "visual": [visual.data for visual in self.visual],
            "collision": [collision.data for collision in self.collision],
            "inertial": self.inertial.data if self.inertial else None,
            "attr": _attr_to_data(self.attr),
            "joints": [joint.data for joint in self.joints],
        }

    @data.setter
    def data(self, data):
        from .joint import Joint

        self.name = data["name"]
        self.type = data["type"]
        self.visual = [Visual.from_data(d) for d in data["visual"]]
        self.collision = [Collision.from_data(d) for d in data["collision"]]
        self.inertial = Inertial.from_data(data["inertial"]) if data["inertial"] else None
        self.attr = _attr_from_data(data["attr"])
        self.joints = [Joint.from_data(d) for d in data["joints"]]

    @classmethod
    def from_data(cls, data):
        link = cls(data["name"])
        link.data = data
        return link


URDFParser.install_parser(Link, "robot/link")
URDFParser.install_parser(Inertial, "robot/link/inertial")
URDFParser.install_parser(Mass, "robot/link/inertial/mass")
URDFParser.install_parser(Inertia, "robot/link/inertial/inertia")

URDFParser.install_parser(Visual, "robot/link/visual")
URDFParser.install_parser(Collision, "robot/link/collision")

URDFParser.install_parser(
    Frame,
    "robot/link/inertial/origin",
    "robot/link/visual/origin",
    "robot/link/collision/origin",
    proxy_type=FrameProxy,
)
URDFParser.install_parser(Geometry, "robot/link/visual/geometry", "robot/link/collision/geometry")
URDFParser.install_parser(
    MeshDescriptor,
    "robot/link/visual/geometry/mesh",
    "robot/link/collision/geometry/mesh",
)
URDFParser.install_parser(
    Box,
    "robot/link/visual/geometry/box",
    "robot/link/collision/geometry/box",
    proxy_type=BoxProxy,
)
URDFParser.install_parser(
    Cylinder,
    "robot/link/visual/geometry/cylinder",
    "robot/link/collision/geometry/cylinder",
    proxy_type=CylinderProxy,
)
URDFParser.install_parser(
    Sphere,
    "robot/link/visual/geometry/sphere",
    "robot/link/collision/geometry/sphere",
    proxy_type=SphereProxy,
)
URDFParser.install_parser(
    Capsule,
    "robot/link/visual/geometry/capsule",
    "robot/link/collision/geometry/capsule",
    proxy_type=CapsuleProxy,
)

URDFParser.install_parser(Material, "robot/link/visual/material")
URDFParser.install_parser(Color, "robot/link/visual/material/color")
URDFParser.install_parser(Texture, "robot/link/visual/material/texture")
