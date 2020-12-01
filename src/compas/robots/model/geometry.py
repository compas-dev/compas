from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

import compas.geometry
from compas.base import Base
from compas.datastructures import Mesh
from compas.files.urdf import URDFElement
from compas.files.urdf import URDFGenericElement
from compas.geometry import Frame
from compas.geometry import Shape
from compas.utilities import hex_to_rgb

__all__ = [
    'Geometry',
    'Box',
    'Cylinder',
    'Sphere',
    'Capsule',
    'MeshDescriptor',
    'Color',
    'Texture',
    'Material',
    'Origin'
]

# Copied from https://github.com/ubernostrum/webcolors/blob/master/webcolors.py
HTML4_NAMES_TO_HEX = {
    u'aqua': u'#00ffff',
    u'black': u'#000000',
    u'blue': u'#0000ff',
    u'fuchsia': u'#ff00ff',
    u'green': u'#008000',
    u'gray': u'#808080',
    u'lime': u'#00ff00',
    u'maroon': u'#800000',
    u'navy': u'#000080',
    u'olive': u'#808000',
    u'purple': u'#800080',
    u'red': u'#ff0000',
    u'silver': u'#c0c0c0',
    u'teal': u'#008080',
    u'white': u'#ffffff',
    u'yellow': u'#ffff00',
}


def _parse_floats(values):
    return [float(i) for i in values.split()]


def _attr_to_data(attr):
    return {k: v.data if hasattr(v, 'data') else v for k, v in attr.items()}


def _generic_from_data_or_data(data):
    try:
        data = URDFGenericElement.from_data(data)
    finally:
        return data


def _attr_from_data(data):
    return {k: _generic_from_data_or_data(d) for k, d in data.items()}


class Origin(Frame):
    """Reference frame represented by an instance of :class:`Frame`.

    An origin is defined by a base point and two orthonormal base vectors.

    Parameters
    ----------
    point : point
        The origin of the origin.
    xaxis : vector
        The x-axis of the origin.
    yaxis : vector
        The y-axis of the origin.

    Examples
    --------
    >>> from compas.geometry import Point
    >>> from compas.geometry import Vector
    >>> o = Origin([0, 0, 0], [1, 0, 0], [0, 1, 0])
    >>> o = Origin(Point(0, 0, 0), Vector(1, 0, 0), Point(0, 1, 0))
    """

    def __init__(self, point, xaxis, yaxis):
        super(Origin, self).__init__(point, xaxis, yaxis)

    def get_urdf_element(self):
        attributes = {
            'xyz': "{} {} {}".format(self.point.x, self.point.y, self.point.z),
            'rpy': "{} {} {}".format(*self.euler_angles())
        }
        return URDFElement('origin', attributes)

    @classmethod
    def from_urdf(cls, attributes, elements, text):
        """Create origin instance from an URDF element.

        Parameters
        ----------
        attributes : dict
            Attributes of the URDF element.
        elements: list of obj
            Children elements of the URDF element.
        text: str or None
            Text content of the URDF element.

        Returns
        -------
        :class:`Origin`
            Origin instance.

        Examples
        --------
        >>> attributes = {'rpy': '0.0 1.57 0.0', 'xyz': '0.0 0.13 0.0'}
        >>> Origin.from_urdf(attributes, [], None)
        Frame(Point(0.000, 0.130, 0.000), Vector(0.001, 0.000, -1.000), Vector(0.000, 1.000, 0.000))
        """
        xyz = _parse_floats(attributes.get('xyz', '0 0 0'))
        rpy = _parse_floats(attributes.get('rpy', '0 0 0'))
        return cls.from_euler_angles(rpy, static=True, axes='xyz', point=xyz)

    def scale(self, factor):
        """Scale the origin by a given factor.

        Parameters
        ----------
        factor : :obj:`float`
            Scale factor.

        Returns
        -------
        None

        Examples
        --------
        >>> o = Origin([0, 0, 0], [1, 0, 0], [0, 1, 0])
        >>> o.scale(10)
        """
        self.point = self.point * factor


class BaseShape(Base):
    """Base class for all 3D shapes.

    Attributes
    ----------
    geometry : :class:`compas.geometry.Shape`
        The COMPAS geometry of this shape.
    """

    def __init__(self):
        super(BaseShape, self).__init__()
        self.geometry = None

    @property
    def data(self):
        raise NotImplementedError

    @data.setter
    def data(self, data):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data):
        raise NotImplementedError

    def to_data(self):
        return self.data

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        return cls.from_data(data)

    def to_json(self, filepath):
        with open(filepath, 'w+') as f:
            json.dump(self.data, f)


class Box(BaseShape):
    """3D shape primitive representing a box.

    Parameters
    ----------
    size : str
        The dimensions of the box in x-, y-, and z-axis, like '1 1 1'.

    Attributes
    ----------
    size : list of 3 float
        The dimensions of the box.
    geometry : :class:`compas.geometry.Box`
        The COMPAS geometry of this box.

    Examples
    --------
    >>> box = Box('1 1 1')
    >>> box.geometry
    Box(Frame(Point(0.000, 0.000, 0.000), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000)), 1.0, 1.0, 1.0)
    """

    def __init__(self, size):
        super(Box, self).__init__()
        self.size = _parse_floats(size)
        self.geometry = compas.geometry.Box(Frame.worldXY(), *self.size)

    def get_urdf_element(self):
        attributes = {'size': '{} {} {}'.format(*self.size)}
        return URDFElement('box', attributes)

    @property
    def data(self):
        return {
            'type': 'box',
            'size': self.size,
            'geometry': self.geometry.data,
        }

    @data.setter
    def data(self, data):
        self.size = data['size']
        self.geometry = compas.geometry.Box.from_data(data['geometry'])

    @classmethod
    def from_data(cls, data):
        box = cls('1 1 1')
        box.data = data
        return box


class Cylinder(BaseShape):
    """3D shape primitive representing a cylinder.

    Parameters
    ----------
    radius : str or float
        The cylinder's radius.
    length : str or float
        The cylinder's length.

    Attributes
    ----------
    radius : float
        The cylinder's radius.
    length : float
        The cylinder's length.
    geometry : :class:`compas.geometry.Cylinder`
        The COMPAS geometry of this cylinder.

    Examples
    --------
    >>> c = Cylinder(1, 4)
    >>> c.geometry
    Cylinder(Circle(Plane(Point(0.000, 0.000, 0.000), Vector(0.000, 0.000, 1.000)), 1.0), 4.0)
    """

    def __init__(self, radius, length):
        super(Cylinder, self).__init__()
        self.radius = float(radius)
        self.length = float(length)
        plane = compas.geometry.Plane([0, 0, 0], [0, 0, 1])
        circle = compas.geometry.Circle(plane, self.radius)
        self.geometry = compas.geometry.Cylinder(circle, self.length)

    def get_urdf_element(self):
        attributes = {'radius': self.radius, 'length': self.length}
        return URDFElement('cylinder', attributes)

    @property
    def data(self):
        return {
            'type': 'cylinder',
            'radius': self.radius,
            'length': self.length,
            'geometry': self.geometry.data,
        }

    @data.setter
    def data(self, data):
        self.radius = data['radius']
        self.length = data['length']
        self.geometry = compas.geometry.Cylinder.from_data(data['geometry'])

    @classmethod
    def from_data(cls, data):
        cyl = cls(data['radius'], data['length'])
        cyl.data = data
        return cyl


class Sphere(BaseShape):
    """3D shape primitive representing a sphere.

    Parameters
    ----------
    radius : str or float
        The sphere's radius.

    Attributes
    ----------
    radius : float
        The sphere's radius.
    geometry : :class:`compas.geometry.Sphere`
        The COMPAS geometry of this sphere.

    Examples
    --------
    >>> s = Sphere(1)
    >>> s.geometry
    Sphere(Point(0.000, 0.000, 0.000), 1.0)
    """

    def __init__(self, radius):
        super(Sphere, self).__init__()
        self.radius = float(radius)
        self.geometry = compas.geometry.Sphere((0, 0, 0), radius)

    def get_urdf_element(self):
        attributes = {'radius': self.radius}
        return URDFElement('sphere', attributes)

    @property
    def data(self):
        return {
            'type': 'sphere',
            'radius': self.radius,
            'geometry': self.geometry.data,
        }

    @data.setter
    def data(self, data):
        self.radius = data['radius']
        self.geometry = compas.geometry.Sphere.from_data(data['geometry'])

    @classmethod
    def from_data(cls, data):
        sph = cls(data['radius'])
        sph.data = data
        return sph


class Capsule(BaseShape):
    """3D shape primitive representing a capsule.

    Parameters
    ----------
    radius : str or float
        The sphere's radius.
    length : str or float
        The sphere's length.

    Attributes
    ----------
    radius : float
        The sphere's radius.
    length : float
        The sphere's length.

    Examples
    --------
    >>> c = Capsule(1, 4)
    """

    def __init__(self, radius, length):
        super(Capsule, self).__init__()
        self.radius = float(radius)
        self.length = float(length)

    def get_urdf_element(self):
        attributes = {'radius': self.radius, 'length': self.length}
        return URDFElement('capsule', attributes)

    @property
    def data(self):
        return {
            'type': 'capsule',
            'radius': self.radius,
            'length': self.length,
        }

    @data.setter
    def data(self, data):
        self.radius = data['radius']
        self.length = data['length']

    @classmethod
    def from_data(cls, data):
        cap = cls(data['radius'], data['length'])
        cap.data = data
        return cap


class MeshDescriptor(BaseShape):
    """Description of a mesh.

    Parameters
    ----------
    filename : str
        The mesh' filename.
    scale : str, optional
        The scale factors of the mesh in the x-, y-, and z-direction.

    Attributes
    ----------
    filename : str
        The mesh' filename.
    scale : list of 3 float
        The scale factors of the mesh in the x-, y-, and z-direction.
    geometry : :class:`compas.datastructures.Mesh`
        The COMPAS geometry of this mesh.

    Examples
    --------
    >>> m = MeshDescriptor('link.stl')
    """

    def __init__(self, filename, scale='1.0 1.0 1.0'):
        super(MeshDescriptor, self).__init__()
        self.filename = filename
        self.scale = _parse_floats(scale)

    def get_urdf_element(self):
        attributes = {'filename': self.filename}
        # There is no need to record default values.  Usually these
        # coincide with some form of 0 and are filtered out with
        # `attributes = dict(filter(lambda x: x[1], attributes.items()))`,
        # but here we must be explicit.
        if self.scale != [1.0, 1.0, 1.0]:
            attributes['scale'] = "{} {} {}".format(*self.scale)
        return URDFElement('mesh', attributes)

    @property
    def data(self):
        return {
            'type': 'mesh',
            'filename': self.filename,
            'scale': self.scale,
            'geometry': self.geometry.data if self.geometry else None,
        }

    @data.setter
    def data(self, data):
        self.filename = data['filename']
        self.scale = data['scale']
        self.geometry = Mesh.from_data(data['geometry']) if data['geometry'] else None

    @classmethod
    def from_data(cls, data):
        md = cls('')
        md.data = data
        return md


class Color(Base):
    """Color represented in RGBA.

    Parameters
    ----------
    rgba : str
        Color values as string.

    Attributes
    ----------
    rgba : list of float
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
        attributes = {'rgba': "{} {} {} {}".format(*self.rgba)}
        return URDFElement('color', attributes)

    @property
    def data(self):
        return {
            'rgba': self.rgba,
        }

    @data.setter
    def data(self, data):
        self.rgba = data['rgba']

    @classmethod
    def from_data(cls, data):
        color = cls('1 1 1')
        color.data = data
        return color

    def to_data(self):
        return self.data

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        return cls.from_data(data)

    def to_json(self, filepath):
        with open(filepath, 'w+') as f:
            json.dump(self.data, f)


class Texture(Base):
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
        attributes = {'filename': self.filename}
        return URDFElement('texture', attributes)

    @property
    def data(self):
        return {
            'filename': self.filename,
        }

    @data.setter
    def data(self, data):
        self.filename = data['filename']

    @classmethod
    def from_data(cls, data):
        return cls(**data)

    def to_data(self):
        return self.data

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        return cls.from_data(data)

    def to_json(self, filepath):
        with open(filepath, 'w+') as f:
            json.dump(self.data, f)


class Material(Base):
    """Material description.

    Parameters
    ----------
    name : str
        The name of the material.
    color : :class:`compas.robots.Color` or None
        The color of the material.
    texture : :class:`compas.robots.Texture` or None
        The filename of the texture.

    Examples
    --------
    >>> c = Color('1 0 0')
    >>> material = Material('wood', c)

    >>> material = Material('aqua')
    >>> material.get_color()
    [0.0, 1.0, 1.0, 1.0]
    """

    def __init__(self, name=None, color=None, texture=None):
        super(Material, self).__init__()
        self.name = name
        self.color = color
        self.texture = texture

    def get_urdf_element(self):
        attributes = {'name': self.name}
        elements = [self.color, self.texture]
        return URDFElement('material', attributes, elements)

    @property
    def data(self):
        return {
            'name': self.name,
            'color': self.color.data,
            'texture': self.texture.data if self.texture else None,
        }

    @data.setter
    def data(self, data):
        self.name = data['name']
        self.color = Color.from_data(data['color'])
        self.texture = Texture.from_data(data['texture']) if data['texture'] else None

    @classmethod
    def from_data(cls, data):
        material = cls()
        material.data = data
        return material

    def to_data(self):
        return self.data

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        return cls.from_data(data)

    def to_json(self, filepath):
        with open(filepath, 'w+') as f:
            json.dump(self.data, f)

    def get_color(self):
        """Get the RGBA color array of the material.

        Returns
        -------
        :obj:`list` of :obj:`float`
            List of 4 floats (``0.0-1.0``) indicating RGB colors and Alpha channel of the material.

        Examples
        --------
        >>> material = Material('aqua')
        >>> material.get_color()
        [0.0, 1.0, 1.0, 1.0]
        """
        if self.name:
            if self.name in HTML4_NAMES_TO_HEX:
                r, g, b = hex_to_rgb(HTML4_NAMES_TO_HEX[self.name])
                return [r / 255., g / 255., b / 255., 1.]
        if self.color:
            return self.color.rgba
        return None


TYPE_CLASS_ENUM = {
    'box': Box,
    'cylinder': Cylinder,
    'sphere': Sphere,
    'capsule': Capsule,
    'mesh': MeshDescriptor,
}


class Geometry(Base):
    """Geometrical description of the shape of a link.

    Parameters
    ----------
    box : :class:`compas.robots.Box` or None
        A box shape primitive.
    cylinder : :class:`compas.robots.Cylinder` or None
        A cylinder shape primitive.
    sphere : :class:`compas.robots.Sphere` or None
        A sphere shape primitive.
    capsule : :class:`compas.robots.Capsule` or None
        A capsule shape primitive.
    mesh : :class:`compas.robots.MeshDescriptor` or None
        A descriptor of a mesh.
    **kwargs : keyword arguments
        Additional attributes

    Attributes
    ----------
    shape : :class:`BaseShape`
        The shape of the geometry
    attr : keyword arguments
        Additional attributes
    geo : :class:`compas.datastructures.Mesh` or :class:`compas.geometry.Shape` or None
        The native geometry object.

    Examples
    --------
    >>> box = Box('1 1 1')
    >>> geo = Geometry(box=box)
    """

    def __init__(self, box=None, cylinder=None, sphere=None, capsule=None, mesh=None, **kwargs):
        super(Geometry, self).__init__()
        self.shape = box or cylinder or sphere or capsule or mesh
        self.attr = kwargs
        if not self.shape:
            raise TypeError(
                'Geometry must define at least one of: box, cylinder, sphere, capsule, mesh')

        if 'geometry' not in dir(self.shape):
            raise TypeError('Shape implementation does not define a geometry accessor')

    def get_urdf_element(self):
        attributes = self.attr.copy()
        elements = [self.shape]
        return URDFElement('geometry', attributes, elements)

    @property
    def data(self):
        return {
            'shape': self.shape.data,
            'attr': _attr_to_data(self.attr),
        }

    @data.setter
    def data(self, data):
        class_ = TYPE_CLASS_ENUM[data['shape']['type']]
        self.shape = class_.from_data(data['shape'])
        self.attr = _attr_from_data(data['attr'])

    @classmethod
    def from_data(cls, data):
        class_ = TYPE_CLASS_ENUM[data['shape']['type']]
        geo = cls(box=class_.from_data(data['shape']))
        geo.data = data
        return geo

    def to_data(self):
        return self.data

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        return cls.from_data(data)

    def to_json(self, filepath):
        with open(filepath, 'w+') as f:
            json.dump(self.data, f)

    @property
    def geo(self):
        """Get geometry associated to this shape.

        Returns
        -------
        object
            Shape's geometry, usually a mesh implementation.
        """
        return self.shape.geometry

    @staticmethod
    def _get_item_meshes(item):
        # NOTE: Currently, shapes assign their meshes to an
        # attribute called `geometry`, but this will change soon to `meshes`.
        # This code handles the situation in a forward-compatible
        # manner. Eventually, this can be simplified to use only `meshes` attr
        if hasattr(item.geometry.shape, 'meshes'):
            meshes = item.geometry.shape.meshes
        else:
            meshes = item.geometry.shape.geometry

        if isinstance(meshes, Shape):
            meshes = [Mesh.from_shape(meshes)]

        if meshes:
            # Coerce meshes into an iterable (a tuple if not natively iterable)
            if not hasattr(meshes, '__iter__'):
                meshes = (meshes,)

        return meshes


if __name__ == '__main__':
    import doctest
    doctest.testmod(globs=globals())
