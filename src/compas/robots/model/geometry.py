from __future__ import absolute_import, division, print_function

from compas.files import URDF
from compas.geometry import Frame

# URDF is defined in meters
# so we scale it all to millimeters
SCALE_FACTOR = 1000

__all__ = ['Geometry',
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


def _parse_floats(values, scale_factor=None):
    result = []

    for i in values.split():
        val = float(i)
        if scale_factor:
            val = val * scale_factor
        result.append(val)

    return result


class Origin(object):
    """Reference frame represented by an instance of :class:`Frame`."""

    @classmethod
    def from_urdf(cls, attributes, elements, text):
        xyz = _parse_floats(attributes.get('xyz', '0 0 0'), SCALE_FACTOR)
        rpy = _parse_floats(attributes.get('rpy', '0 0 0'))
        return Frame.from_euler_angles(rpy, static=True, axes='xyz', point=xyz)


class Box(object):
    """3D shape primitive representing a box."""

    def __init__(self, size):
        self.size = _parse_floats(size, SCALE_FACTOR)


class Cylinder(object):
    """3D shape primitive representing a cylinder."""

    def __init__(self, radius, length):
        self.radius = float(radius) * SCALE_FACTOR
        self.length = float(length) * SCALE_FACTOR


class Sphere(object):
    """3D shape primitive representing a sphere."""

    def __init__(self, radius):
        self.radius = float(radius) * SCALE_FACTOR


class Capsule(Cylinder):
    """3D shape primitive representing a capsule."""

    def __init__(self, radius, length):
        self.radius = float(radius) * SCALE_FACTOR
        self.length = float(length) * SCALE_FACTOR


class MeshDescriptor(object):
    """Description of a mesh."""

    def __init__(self, filename, scale='1.0 1.0 1.0'):
        self.filename = filename
        self.scale = _parse_floats(scale)


class Color(object):
    """Color represented in RGBA."""

    def __init__(self, rgba):
        self.rgba = _parse_floats(rgba)


class Texture(object):
    """Texture description."""

    def __init__(self, filename):
        self.filename = filename


class Material(object):
    """Material description."""

    def __init__(self, name=None, color=None, texture=None):
        self.name = name
        self.color = color
        self.texture = texture


class Geometry(object):
    """Shape of a link."""

    def __init__(self, box=None, cylinder=None, sphere=None, capsule=None, mesh=None, **kwargs):
        self.shape = box or cylinder or sphere or capsule or mesh
        self.attr = kwargs
        if not self.shape:
            raise TypeError(
                'Geometry must define at least one of: box, cylinder, sphere, capsule, mesh')
