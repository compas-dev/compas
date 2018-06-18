from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from System.Drawing.Color import FromArgb
    from System.Collections.Generic import List

except ImportError:
    import sys
    if 'ironpython' in sys.version.lower():
        raise


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['FacesConduit', ]


class FacesConduit(Conduit):
    """A Rhino display conduit for faces.

    Parameters:
        labels (list): A list of label tuples. Each tuple contains a position and text for the label.
        color (tuple): Optional.
            RGB color spec for the dots.
            Default is ``None``.

    Example:

        .. code-block:: python

            import time
            from compas.geometry.elements import Polyhedron

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
    def __init__(self, vertices, faces, **kwargs):
        super(FacesConduit, self).__init__(**kwargs)
        self.vertices = vertices
        self.faces = faces
        self._default_color = FromArgb(255, 255, 255)
        self.colors = None

    def DrawForeground(self, e):
        for i, face in enumerate(self.faces):
            points = [Point3d(* self.vertices[key]) for key in face]
            if self.colors:
                e.Display.DrawPolygon(points, self.colors[i], True)
            else:
                e.Display.DrawPolygon(points, self._default_color, True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import time
    from compas.geometry.elements import Polyhedron

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
