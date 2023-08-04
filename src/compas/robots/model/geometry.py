from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas.colors
import compas.geometry

from compas.data import Data
from compas.datastructures import Mesh
from compas.files import URDFElement
from compas.geometry import Frame

from .base import ProxyObject
from .base import _attr_from_data
from .base import _attr_to_data
from .base import _parse_floats


class BoxProxy(ProxyObject):
    """Proxy class that adds URDF functionality to an instance of :class:`~compas.geometry.Box`.

    This class is internal and not intended to be referenced externally.
    """

    def get_urdf_element(self):
        attributes = {"size": "{} {} {}".format(*self.size)}
        return URDFElement("box", attributes)

    @classmethod
    def from_urdf(cls, attributes, elements=None, text=None):
        size = _parse_floats(attributes["size"])
        return cls(compas.geometry.Box(Frame.worldXY(), *size))

    @property
    def meshes(self):
        return [Mesh.from_shape(self)]

    @property
    def size(self):
        return [self.xsize, self.ysize, self.zsize]


class CylinderProxy(ProxyObject):
    """Proxy class that adds URDF functionality to an instance of :class:`~compas.geometry.Cylinder`.

    This class is internal and not intended to be referenced externally.
    """

    def get_urdf_element(self):
        attributes = {"radius": self.radius, "length": self.length}
        return URDFElement("cylinder", attributes)

    @classmethod
    def from_urdf(cls, attributes, elements=None, text=None):
        radius = float(attributes["radius"])
        length = float(attributes["length"])
        frame = compas.geometry.Frame.worldXY()
        return cls(compas.geometry.Cylinder(frame, radius=radius, height=length))

    @property
    def meshes(self):
        return [Mesh.from_shape(self)]

    @property
    def length(self):
        return self.height


class SphereProxy(ProxyObject):
    """Proxy class that adds URDF functionality to an instance of :class:`~compas.geometry.Sphere`.

    This class is internal and not intended to be referenced externally.
    """

    def get_urdf_element(self):
        attributes = {"radius": self.radius}
        return URDFElement("sphere", attributes)

    @classmethod
    def from_urdf(cls, attributes, elements=None, text=None):
        radius = float(attributes["radius"])
        return cls(compas.geometry.Sphere(compas.geometry.Frame.worldXY(), radius))

    @property
    def meshes(self):
        return [Mesh.from_shape(self)]


class CapsuleProxy(ProxyObject):
    """Proxy class that adds URDF functionality to an instance of :class:`~compas.geometry.Capsule`.

    This class is internal and not intended to be referenced externally.
    """

    def get_urdf_element(self):
        attributes = {"radius": self.radius, "length": self.length}
        return URDFElement("capsule", attributes)

    @classmethod
    def from_urdf(cls, attributes, elements=None, text=None):
        radius = float(attributes["radius"])
        length = float(attributes["length"])
        frame = compas.geometry.Frame.worldXY()
        return cls(compas.geometry.Capsule(frame, radius=radius, height=length))

    @property
    def meshes(self):
        return [Mesh.from_shape(self)]


class MeshDescriptor(Data):
    """Description of a mesh.

    Parameters
    ----------
    filename : str
        The mesh' filename.
    scale : str, optional
        The scale factors of the mesh in the x-, y-, and z-direction.
    **kwargs : dict[str, Any], optional
        The keyword arguments (kwargs) collected in a dict.
        These allow using non-standard attributes absent in the URDF specification.

    Attributes
    ----------
    filename : str
        The mesh' filename.
    scale : [float, float, float]
        The scale factors of the mesh in the x-, y-, and z-direction.
    meshes : list[:class:`~compas.datastructures.Mesh`]
        List of COMPAS geometric meshes.

    Examples
    --------
    >>> m = MeshDescriptor('link.stl')

    """

    def __init__(self, filename, scale="1.0 1.0 1.0", **kwargs):
        super(MeshDescriptor, self).__init__()
        self.filename = filename
        self.scale = _parse_floats(scale)
        self.meshes = []
        self.attr = kwargs or {}

    def get_urdf_element(self):
        attributes = {"filename": self.filename}
        # There is no need to record default values.  Usually these
        # coincide with some form of 0 and are filtered out with
        # `attributes = dict(filter(lambda x: x[1], attributes.items()))`,
        # but here we must be explicit.
        if self.scale != [1.0, 1.0, 1.0]:
            attributes["scale"] = "{} {} {}".format(*self.scale)
        attributes.update(self.attr)
        return URDFElement("mesh", attributes)

    @property
    def data(self):
        return {
            "filename": self.filename,
            "scale": self.scale,
            "attr": _attr_to_data(self.attr),
            "meshes": self.meshes,
        }

    @data.setter
    def data(self, data):
        self.filename = data["filename"]
        self.scale = data["scale"]
        self.attr = _attr_from_data(data["attr"]) if "attr" in data else {}
        self.meshes = data["meshes"]

    @classmethod
    def from_data(cls, data):
        md = cls("")
        md.data = data
        return md


class Color(Data):
    """Color represented in RGBA.

    Parameters
    ----------
    rgba : str
        Color values as string.

    Attributes
    ----------
    rgba : [float, float, float, float]
        Color values as list of float

    Examples
    --------
    >>> c = Color('1 0 0')
    >>> c.rgba
    [1.0, 0.0, 0.0]

    """

    def __init__(self, rgba):
        super(Color, self).__init__()
        self.rgba = _parse_floats(rgba)

    def get_urdf_element(self):
        attributes = {"rgba": "{} {} {} {}".format(*self.rgba)}
        return URDFElement("color", attributes)

    @property
    def data(self):
        return {
            "rgba": self.rgba,
        }

    @data.setter
    def data(self, data):
        self.rgba = data["rgba"]

    @classmethod
    def from_data(cls, data):
        color = cls("1 1 1")
        color.data = data
        return color


class Texture(Data):
    """Texture description.

    Parameters
    ----------
    filename : str
        The filename of the texture.

    Attributes
    ----------
    filename : str
        The filename of the texture.

    Examples
    --------
    >>> t = Texture('wood.jpg')

    """

    def __init__(self, filename):
        super(Texture, self).__init__()
        self.filename = filename

    def get_urdf_element(self):
        attributes = {"filename": self.filename}
        return URDFElement("texture", attributes)

    @property
    def data(self):
        return {
            "filename": self.filename,
        }

    @data.setter
    def data(self, data):
        self.filename = data["filename"]

    @classmethod
    def from_data(cls, data):
        return cls(**data)


class Material(Data):
    """Material description.

    Parameters
    ----------
    name : str
        The name of the material.
    color : :class:`~compas.robots.Color`, optional
        The color of the material.
    texture : :class:`~compas.robots.Texture`, optional
        The filename of the texture.

    Examples
    --------
    >>> c = Color('1 0 0')
    >>> material = Material('wood', c)

    >>> material = Material('aqua')
    >>> material.get_color()
    (0.0, 1.0, 1.0, 1.0)

    """

    def __init__(self, name=None, color=None, texture=None):
        super(Material, self).__init__()
        self.name = name
        self.color = color
        self.texture = texture

    def get_urdf_element(self):
        attributes = {"name": self.name}
        elements = [self.color, self.texture]
        return URDFElement("material", attributes, elements)

    @property
    def data(self):
        return {
            "name": self.name,
            "color": self.color.data if self.color else None,
            "texture": self.texture.data if self.texture else None,
        }

    @data.setter
    def data(self, data):
        self.name = data["name"]
        self.color = Color.from_data(data["color"]) if data["color"] else None
        self.texture = Texture.from_data(data["texture"]) if data["texture"] else None

    def get_color(self):
        """Get the RGBA color array of the material.

        Returns
        -------
        [float, float, float, float]
            List of 4 floats (``0.0-1.0``) indicating RGB colors and Alpha channel of the material.

        Examples
        --------
        >>> material = Material('aqua')
        >>> material.get_color()
        (0.0, 1.0, 1.0, 1.0)

        """
        if self.name:
            try:
                color = compas.colors.Color.from_name(self.name)
                return color.rgba
            except ValueError:
                pass
        if self.color:
            return self.color.rgba
        return None


TYPE_CLASS_ENUM = {
    "box": compas.geometry.Box,
    "cylinder": compas.geometry.Cylinder,
    "sphere": compas.geometry.Sphere,
    "capsule": compas.geometry.Capsule,
    "mesh": MeshDescriptor,
}

# TYPE_CLASS_ENUM_BY_DATA = {
#     ("frame", "xsize", "ysize", "zsize"): compas.geometry.Box,
#     ("circle", "height"): compas.geometry.Cylinder,
#     ("point", "radius"): compas.geometry.Sphere,
#     ("line", "radius"): compas.geometry.Capsule,
#     ("attr", "filename", "scale"): MeshDescriptor,
#     ("attr", "filename", "meshes", "scale"): MeshDescriptor,
# }


# def _get_type_from_shape_data(data):
#     # This is here only to support models serialized with older versions of COMPAS
#     if "type" in data:
#         return TYPE_CLASS_ENUM[data["type"]]

#     # The current scenario is that we need to figure out the object type based on the DATASCHEMA
#     keys = tuple(sorted(data.keys()))
#     return TYPE_CLASS_ENUM_BY_DATA[keys]


class Geometry(Data):
    """Geometrical description of the shape of a link.

    Parameters
    ----------
    box : :class:`~compas.geometry.Box`, optional
        A box shape primitive.
    cylinder : :class:`~compas.geometry.Cylinder`, optional
        A cylinder shape primitive.
    sphere : :class:`~compas.geometry.Sphere`, optional
        A sphere shape primitive.
    capsule : :class:`~compas.geometry.Capsule`, optional
        A capsule shape primitive.
    mesh : :class:`~compas.robots.MeshDescriptor`, optional
        A descriptor of a mesh.
    **kwargs : dict[str, Any], optional
        The keyword arguments (kwargs) collected in a dict.
        These allow using non-standard attributes absent in the URDF specification.

    Attributes
    ----------
    shape : object
        The shape of the geometry
    attr : keyword arguments
        Additional attributes

    Examples
    --------
    >>> box = compas.geometry.Box(Frame.worldXY(), 1, 1, 1)
    >>> geo = Geometry(box=box)

    """

    def __init__(self, box=None, cylinder=None, sphere=None, capsule=None, mesh=None, **kwargs):
        super(Geometry, self).__init__()
        self.shape = box or cylinder or sphere or capsule or mesh
        self.attr = kwargs

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        if value is None:
            self._shape = None
            return

        if isinstance(value, compas.geometry.Box):
            self._shape = BoxProxy.create_proxy(value)
        elif isinstance(value, compas.geometry.Cylinder):
            self._shape = CylinderProxy.create_proxy(value)
        elif isinstance(value, compas.geometry.Sphere):
            self._shape = SphereProxy.create_proxy(value)
        elif isinstance(value, compas.geometry.Capsule):
            self._shape = CapsuleProxy.create_proxy(value)
        else:
            self._shape = value

        if "meshes" not in dir(self._shape):
            raise TypeError("Shape implementation does not define a meshes accessor: {}".format(type(self._shape)))

    def get_urdf_element(self):
        attributes = self.attr.copy()
        elements = [self.shape]
        return URDFElement("geometry", attributes, elements)

    @property
    def data(self):
        return {
            "shape": self.shape,  # type: ignore
            "attr": _attr_to_data(self.attr),
        }

    @data.setter
    def data(self, data):
        # class_ = _get_type_from_shape_data(data["shape"])
        self.shape = data["shape"]
        self.attr = _attr_from_data(data["attr"])

    @classmethod
    def from_data(cls, data):
        # class_ = _get_type_from_shape_data(data["shape"])
        geo = cls(box=data["shape"])
        geo.data = data
        return geo

    @staticmethod
    def _get_item_meshes(item):
        meshes = item.geometry.shape.meshes

        if meshes:
            # Coerce meshes into an iterable (a tuple if not natively iterable)
            if not hasattr(meshes, "__iter__"):
                meshes = (meshes,)

        return meshes


# Deprecated: this are aliases for backwards compatibility, but need to be removed on 2.x
Origin = Frame
Cylinder = CylinderProxy
Box = BoxProxy
Sphere = SphereProxy
Capsule = CapsuleProxy
