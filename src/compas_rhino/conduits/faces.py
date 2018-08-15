from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas.utilities import colour_to_rgb

from compas_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from System.Drawing.colour import FromArgb
    from System.Collections.Generic import List

except ImportError:
    compas.raise_if_ironpython()


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['FacesConduit', ]


class FacesConduit(Conduit):
    """A Rhino display conduit for faces.

    Parameters
    ----------
    vertices : list of list of float
        The coordinates of the vertices of the faces.
    faces : list of list of int
        The faces defined as lists of indices in ``vertices``.
    colour : list of str or 3-tuple, optional
        The colours of the faces.
        Default is ``None``, in which case the default colour is used for all faces.

    Attributes
    ----------
    colour
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
    def __init__(self, vertices, faces, colour=None, **kwargs):
        super(FacesConduit, self).__init__(**kwargs)
        self._default_colour = FromArgb(255, 255, 255)
        self._colour = None
        self.vertices = vertices or []
        self.faces = faces or []
        self.colour = colour

    @property
    def colour(self):
        """list : Individual face colours.

        Parameters
        ----------
        colour : list of str or 3-tuple
            The colour specification of each face in hex or RGB(255) format.

        """
        return self._colour
    
    @colour.setter
    def colour(self, colour):
        if colour:
            colour[:] = [FromArgb(* colour_to_rgb(c)) for c in colour]
            f = len(self.faces)
            c = len(colour)
            if c < f:
                colour += [self._default_colour for i in range(f - c)]
            elif c > f:
                colour[:] = colour[:f]
            self._colour = colour

    def DrawForeground(self, e):
        for i, face in enumerate(self.faces):
            points = [Point3d(* self.vertices[key]) for key in face]
            if self.colour:
                e.Display.DrawPolygon(points, self.colour[i], True)
            else:
                e.Display.DrawPolygon(points, self._default_colour, True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import time
    from compas.geometry import Polyhedron

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
        print(e)

    finally:
        conduit.disable()
        del conduit
