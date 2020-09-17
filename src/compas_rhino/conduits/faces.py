from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    basestring
except NameError:
    basestring = str

from System.Drawing.Color import FromArgb
from Rhino.Geometry import Point3d

from compas.utilities import color_to_rgb
from compas_rhino.conduits.base import BaseConduit


__all__ = ['FacesConduit']


class FacesConduit(BaseConduit):
    """A Rhino display conduit for faces.

    Parameters
    ----------
    vertices : list of list of float
        The coordinates of the vertices of the faces.
    faces : list of list of int
        The faces defined as lists of indices in ``vertices``.
    color : list of str or 3-tuple, optional
        The colors of the faces.
        Default is ``None``, in which case the default color is used for all faces.

    Attributes
    ----------
    color : list of RGB colors
        The color specification per face.
    vertices : list of list of float
        The coordinates of the vertices of the faces.
    faces : list of list of int
        The faces defined as lists of indices in ``vertices``.

    Examples
    --------
    .. code-block:: python

        from compas.geometry import Polyhedron
        from compas_rhino.conduits import FacesConduit

        polyhedron = Polyhedron.generate(6)
        faces = polyhedron.faces
        vertices = polyhedron.vertices
        polygons = [[vertices[index] for index in face] for face in faces]
        conduit = FacesConduit(polygons)

        with conduit.enabled():
            conduit.redraw(pause=5.0)

    """
    def __init__(self, vertices, faces, color=None, **kwargs):
        super(FacesConduit, self).__init__(**kwargs)
        self._default_color = FromArgb(255, 255, 255)
        self._color = None
        self.vertices = vertices or []
        self.faces = faces or []
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if not color:
            return
        f = len(self.faces)
        if isinstance(color, (basestring, tuple)):
            color = [color for _ in range(f)]
        color = [FromArgb(* color_to_rgb(c)) for c in color]
        c = len(color)
        if c < f:
            color += [self._default_color for _ in range(f - c)]
        elif c > f:
            color[:] = color[:f]
        self._color = color

    def DrawForeground(self, e):
        for i, face in enumerate(self.faces):
            points = [Point3d(* self.vertices[key]) for key in face]
            if self.color:
                e.Display.DrawPolygon(points, self.color[i], True)
            else:
                e.Display.DrawPolygon(points, self._default_color, True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
