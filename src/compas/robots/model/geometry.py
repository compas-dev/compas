from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities.colors import hex_to_rgb
from compas.geometry import Frame
from compas.geometry import Transformation

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


class Origin(Frame):
    """Reference frame represented by an instance of :class:`Frame`."""

    def __init__(self, point, xaxis, yaxis):
        super(Origin, self).__init__(point, xaxis, yaxis)
        self.init = None  # keep a copy to the initial, not transformed origin

    @classmethod
    def from_urdf(cls, attributes, elements, text):
        xyz = _parse_floats(attributes.get('xyz', '0 0 0'))
        rpy = _parse_floats(attributes.get('rpy', '0 0 0'))
        return cls.from_euler_angles(rpy, static=True, axes='xyz', point=xyz)

    @property
    def init_transformation(self):
        return Transformation.from_frame(self.init)

    def create(self, transformation):
        self.transform(transformation)
        self.init = self.copy()

    def reset_transform(self):
        if self.init:
            # TODO: Transform back into initial state does not always work...
            # T = init_transformation * Transformation.from_frame(self).inverse()
            # self.transform(T)
            cp = self.init.copy()
            self.point = cp.point
            self.xaxis = cp.xaxis
            self.yaxis = cp.yaxis

    def scale(self, factor):
        self.point = self.point * factor
        self.init = self.copy()

class Box(object):
    """3D shape primitive representing a box."""

    def __init__(self, size):
        self.size = _parse_floats(size)
        self.geometry = None

    def create(self, urdf_importer, meshcls):
        pass

    def transform(self, transformation):
        if self.geometry:
            self.geometry.transform(transformation)

    def set_color(self, color_rgba):
        pass

    def draw(self):
        if self.geometry:
            return self.geometry.draw()


class Cylinder(object):
    """3D shape primitive representing a cylinder."""

    def __init__(self, radius, length):
        self.radius = float(radius)
        self.length = float(length)
        self.geometry = None

    def create(self, urdf_importer, meshcls):
        pass

    def transform(self, transformation):
        if self.geometry:
            self.geometry.transform(transformation)

    def set_color(self, color_rgba):
        pass

    def draw(self):
        if self.geometry:
            return self.geometry.draw()


class Sphere(object):
    """3D shape primitive representing a sphere."""

    def __init__(self, radius):
        self.radius = float(radius)
        self.geometry = None

    def create(self, urdf_importer, meshcls):
        pass

    def transform(self, transformation):
        if self.geometry:
            self.geometry.transform(transformation)

    def set_color(self, color_rgba):
        pass

    def draw(self):
        if self.geometry:
            return self.geometry.draw()


class Capsule(object):
    """3D shape primitive representing a capsule."""

    def __init__(self, radius, length):
        self.radius = float(radius)
        self.length = float(length)
        self.geometry = None

    def create(self, urdf_importer, meshcls):
        pass

    def transform(self, transformation):
        if self.geometry:
            self.geometry.transform(transformation)

    def set_color(self, color_rgba):
        pass

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
        print("Created mesh from file %s" % self.filename)  # TODO: use logging?

    def transform(self, transformation):
        if self.geometry:
            self.geometry.transform(transformation)

    def set_color(self, color_rgba):
        if self.geometry:
            self.geometry.set_color(color_rgba)

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

    def get_color(self):
        if self.name:
            if self.name in HTML4_NAMES_TO_HEX:
                r, g, b = hex_to_rgb(HTML4_NAMES_TO_HEX[self.name])
                return [r/255., g/255., b/255., 1.]
        if self.color:
            return self.color.rgba
        return None


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
