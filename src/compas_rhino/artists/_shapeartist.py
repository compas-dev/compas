from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import is_color_rgb
from ._artist import Artist


__all__ = ['ShapeArtist']


class ShapeArtist(Artist):
    """Base class for artists for geometric shapes.

    Parameters
    ----------
    shape: :class:`compas.geometry.Shape`
        The geometry of the shape.
    color : tuple, optional
        The RGB color.
    layer : str, optional
        The layer in which the shape should be drawn.

    Attributes
    ----------
    shape: :class:`compas.geometry.Shape`
        The geometry of the shape.
    color : tuple
        The RGB color.
    layer : str
        The layer in which the shape should be drawn.

    Examples
    --------
    .. code-block:: python

        import random
        import compas_rhino

        from compas.geometry import Point, Line, Plane, Circle
        from compas.geometry import Frame, Box, Capsule, Cone, Cylinder, Polyhedron, Sphere, Torus
        from compas.geometry import Pointcloud, Translation
        from compas.utilities import i_to_rgb

        from compas_rhino.artists import BoxArtist, CapsuleArtist, ConeArtist, CylinderArtist, PolyhedronArtist, SphereArtist, TorusArtist

        compas_rhino.clear()

        box = Box(Frame.worldXY(), 0.7, 0.7, 0.7)
        capsule = Capsule(Line(Point(0, 0, 0), Point(0, 0, 1)), 0.2)
        cone = Cone(Circle(Plane([0, 0, 0], [0, 0, 1]), 0.4), 1.0)
        cylinder = Cylinder(Circle(Plane([0, 0, 0], [0, 0, 1]), 0.2), 1.0)
        polyhedron = Polyhedron.from_platonicsolid(4)
        sphere = Sphere(Point(0, 0, 0), 0.4)
        torus = Torus(Plane([0, 0, 0], [0, 0, 1]), 0.5, 0.2)

        templates = [
            (box, BoxArtist, box.frame.point),
            (capsule, CapsuleArtist, capsule.line.midpoint),
            (cone, ConeArtist, cone.circle.plane.point),
            (cylinder, CylinderArtist, cylinder.circle.plane.point),
            (polyhedron, PolyhedronArtist, Point(0, 0, 0)),
            (sphere, SphereArtist, sphere.point),
            (torus, TorusArtist, torus.plane.point),
        ]

        for point in Pointcloud.from_bounds(10, 10, 10, 30):
            tpl, Artist, base = random.choice(templates)
            item = tpl.transformed(Translation.from_vector(point - base))
            artist = Artist(item)
            artist.color = i_to_rgb(random.random())
            artist.draw()

        compas_rhino.update()

    """

    default_color = (255, 255, 255)

    def __init__(self, shape, color=None, layer=None):
        super(ShapeArtist, self).__init__(layer=layer)
        self._u = None
        self._v = None
        self._shape = None
        self._color = None
        self.shape = shape
        self.color = color

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape

    @property
    def color(self):
        if not self._color:
            self._color = self.default_color
        return self._color

    @color.setter
    def color(self, color):
        if is_color_rgb(color):
            self._color = color

    @property
    def u(self):
        if not self._u:
            self._u = 16
        return self._u

    @u.setter
    def u(self, u):
        if u > 2:
            self._u = u

    @property
    def v(self):
        if not self._v:
            self._v = 16
        return self._v

    @v.setter
    def v(self, v):
        if v > 2:
            self._v = v

    def draw(self):
        """Draw the item associated with the artist.

        Returns
        -------
        str
            The GUID of the object created in Rhino.
        """
        pass
