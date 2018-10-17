from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas.utilities import color_to_rgb

from compas_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from System.Drawing.Color import FromArgb
    from System.Collections.Generic import List

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['FacesConduit']


class FacesConduit(Conduit):
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
    color
    vertices : list of list of float
        The coordinates of the vertices of the faces.
    faces : list of list of int
        The faces defined as lists of indices in ``vertices``.

    Example
    -------
    .. code-block:: python

        import time
        from compas.geometry import Polyhedron
        from compas_rhino.conduits import FacesConduit

        polyhedron = Polyhedron.generate(6)

        faces = polyhedron.faces
        vertices = polyhedron.vertices

        polygons = [[vertices[index] for index in face] for face in faces]

        try:
            conduit = FacesConduit(polygons)
            conduit.enable()
            conduit.redraw()
            time.sleep(5.0)

        except Exception as e:
            print e

        finally:
            conduit.disable()
            del conduit

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
        """list : Individual face colors.

        Parameters
        ----------
        color : list of str or 3-tuple
            The color specification of each face in hex or RGB(255) format.

        """
        return self._color
    
    @color.setter
    def color(self, color):
        if color:
            f = len(self.faces)
            if isinstance(color, (basestring, tuple)):
                # if a single color was provided
                color = [color for _ in range(f)]
            # convert to windows system colors
            color = [FromArgb(* color_to_rgb(c)) for c in color]
            # pad the color specification
            c = len(color)
            if c < f:
                color += [self._default_color for _ in range(f - c)]
            elif c > f:
                color[:] = color[:f]
            # assign to the protected value
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

    from random import shuffle
    from compas.geometry import Polyhedron

    polyhedron = Polyhedron.generate(6)

    faces = polyhedron.faces
    vertices = polyhedron.vertices
    colors = [(255, 255, 255), (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255)]

    conduit = FacesConduit(vertices, faces, color=colors)

    with conduit.enabled():
        for i in range(10):
            shuffle(colors)
            conduit.color = colors
            conduit.redraw(pause=1.0)
