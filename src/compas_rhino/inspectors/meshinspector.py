from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas_rhino.conduits import Conduit
from compas_rhino.ui.mouse import Mouse

from compas.geometry import length_vector
from compas.geometry import cross_vectors
from compas.geometry import subtract_vectors

try:
    from Rhino.Geometry import Point3d

    from System.Drawing.Color import FromArgb

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['MeshVertexInspector']


class MeshVertexInspector(Conduit):
    """"""
    def __init__(self, mesh, tol=0.1, dotcolor=None, textcolor=None, **kwargs):
        super(MeshVertexInspector, self).__init__(**kwargs)
        self.mesh      = mesh
        self.tol       = tol
        dotcolor       = dotcolor or (255, 0, 0)
        textcolor      = textcolor or (0, 0, 0)
        self.dotcolor  = FromArgb(*dotcolor)
        self.textcolor = FromArgb(*textcolor)
        self.mouse     = Mouse(self)

    def enable(self):
        self.mouse.Enabled = True
        self.Enabled = True

    def disable(self):
        self.mouse.Enabled = False
        self.Enabled = False

    def DrawForeground(self, e):
        p1  = self.mouse.p1
        p2  = self.mouse.p2
        v12 = subtract_vectors(p2, p1)
        l12 = length_vector(v12)
        for index, (key, attr) in enumerate(self.mesh.vertices(True)):
            p0   = attr['x'], attr['y'], attr['z']
            text = str(index)
            v01  = subtract_vectors(p1, p0)
            v02  = subtract_vectors(p2, p0)
            l    = length_vector(cross_vectors(v01, v02))
            if l12 == 0.0 or (l / l12) < self.tol:
                point = Point3d(*p0)
                e.Display.DrawDot(point, text, self.dotcolor, self.textcolor)
                break


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    import compas_rhino
    from compas.datastructures import Mesh
    from compas_rhino import MeshArtist


    class Mouse(compas_rhino.ui.Mouse):

        def OnMouseDown(self, e):
            self.parent.disable()


    mesh = Mesh.from_obj(compas.get('hypar.obj'))

    artist = MeshArtist(mesh, layer='Inspector')
    artist.clear_layer()
    artist.draw_faces()
    artist.draw_edges()
    artist.draw_vertices()
    artist.redraw()

    inspector = MeshVertexInspector(mesh)
    inspector.enable()
