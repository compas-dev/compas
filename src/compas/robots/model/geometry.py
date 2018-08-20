from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.files import URDF
from compas.geometry import Frame
from compas.geometry.xforms import Scale
from compas.geometry.xforms import Transformation

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


class Origin(Frame):
    """Reference frame represented by an instance of :class:`Frame`."""

    def __init__(self, point, xaxis, yaxis):
        super(Origin, self).__init__(point, xaxis, yaxis)
        self.init = None  # keep a copy to the initial, not transformed origin
        self.init_transformation = None

    @classmethod
    def from_urdf(cls, attributes, elements, text):
        xyz = _parse_floats(attributes.get('xyz', '0 0 0'), SCALE_FACTOR)
        rpy = _parse_floats(attributes.get('rpy', '0 0 0'))
        return cls.from_euler_angles(rpy, static=True, axes='xyz', point=xyz)

    def create(self, transformation):
        self.transform(transformation)
        self.init = self.copy()
        self.init_transformation = Transformation.from_frame(self)

    def reset_transform(self):
        if self.init:
            # TODO: Transform back into initial state does not always work...
            # T = init_transformation * Transformation.from_frame(self).inverse()
            # self.transform(T)
            cp = self.init.copy()
            self.point = cp.point
            self.xaxis = cp.xaxis
            self.yaxis = cp.yaxis


class Box(object):
    """3D shape primitive representing a box."""

    def __init__(self, size):
        self.size = _parse_floats(size, SCALE_FACTOR)
        self.geometry = None

    def create(self, urdf_importer, meshcls):
        pass

    def transform(self, transformation):
        if self.geometry:
            self.geometry.transform(transformation)

    def draw(self):
        if self.geometry:
            return self.geometry.draw()


class Cylinder(object):
    """3D shape primitive representing a cylinder."""

    def __init__(self, radius, length):
        self.radius = float(radius) * SCALE_FACTOR
        self.length = float(length) * SCALE_FACTOR
        self.geometry = None

    def create(self, urdf_importer, meshcls):
        pass

    def transform(self, transformation):
        if self.geometry:
            self.geometry.transform(transformation)

    def draw(self):
        if self.geometry:
            return self.geometry.draw()


class Sphere(object):
    """3D shape primitive representing a sphere."""

    def __init__(self, radius):
        self.radius = float(radius) * SCALE_FACTOR
        self.geometry = None

    def create(self, urdf_importer, meshcls):
        pass

    def transform(self, transformation):
        if self.geometry:
            self.geometry.transform(transformation)

    def draw(self):
        if self.geometry:
            return self.geometry.draw()


class Capsule(object):
    """3D shape primitive representing a capsule."""

    def __init__(self, radius, length):
        self.radius = float(radius) * SCALE_FACTOR
        self.length = float(length) * SCALE_FACTOR
        self.geometry = None

    def create(self, urdf_importer, meshcls):
        pass

    def transform(self, transformation):
        if self.geometry:
            self.geometry.transform(transformation)

    def draw(self):
        if self.geometry:
            return self.geometry.draw()


class MeshDescriptor(object):
    """Description of a mesh."""

    def __init__(self, filename, scale='1.0 1.0 1.0'):
        self.filename = filename
        self.scale = _parse_floats(scale)
        self.geometry = None

    def create(self, urdf_importer, meshcls):
        """Creates the mesh geometry based on the passed urdf_importer and the
        mesh class.
        """
        self.geometry = urdf_importer.read_mesh_from_resource_file_uri(self.filename, meshcls)
        self.set_scale(SCALE_FACTOR)
        print("Created mesh from file %s" % self.filename) # TODO: use logging?

    def transform(self, transformation):
        if self.geometry:
            self.geometry.transform(transformation)

    def set_scale(self, factor):
        S = Scale([factor, factor, factor])
        self.transform(S)

    def draw(self):
        if self.geometry:
            return self.geometry.draw()


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

    def draw(self):
        return self.shape.draw()
