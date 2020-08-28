from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from System.Collections.Generic import List
from System.Drawing.Color import FromArgb
from Rhino.Geometry import Point3d
from Rhino.Geometry import Line

from compas_rhino.conduits import BaseConduit
from compas_rhino.ui import Mouse

from compas.geometry import length_vector
from compas.geometry import cross_vectors
from compas.geometry import subtract_vectors


__all__ = ['MeshVertexInspector']


class MeshVertexInspector(BaseConduit):
    """Inspect mesh topology at the vertices.

    Parameters
    ----------
    mesh: :class:`compas.datastructures.Mesh`
    tol: float, optional
    dotcolor: rgb-tuple, optional
    textcolor: rgb-tuple, optional
    linecolor: rgb-tuple, optional
    """

    def __init__(self, mesh, tol=0.1, dotcolor=None, textcolor=None, linecolor=None, **kwargs):
        super(MeshVertexInspector, self).__init__(**kwargs)
        self._vertex_xyz = None
        dotcolor = dotcolor or (255, 255, 0)
        textcolor = textcolor or (0, 0, 0)
        linecolor = linecolor or (255, 255, 0)
        self.mesh = mesh
        self.tol = tol
        self.dotcolor = FromArgb(*dotcolor)
        self.textcolor = FromArgb(*textcolor)
        self.linecolor = FromArgb(*linecolor)
        self.mouse = Mouse(self)
        self.vertex_nbr = {
            vertex: [(vertex, nbr) if mesh.has_edge((vertex, nbr)) else (nbr, vertex) for nbr in mesh.vertex_neighbors(vertex)]
            for vertex in mesh.vertices()
        }

    @property
    def vertex_xyz(self):
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.mesh.vertex_attributes(vertex, 'xyz') for vertex in self.mesh.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz

    def enable(self):
        """Enable the conduit."""
        self.mouse.Enabled = True
        self.Enabled = True

    def disable(self):
        """Disable the conduit."""
        self.mouse.Enabled = False
        self.Enabled = False

    def DrawForeground(self, e):
        draw_dot = e.Display.DrawDot
        draw_arrows = e.Display.DrawArrows
        a = self.mouse.p1
        b = self.mouse.p2
        ab = subtract_vectors(b, a)
        Lab = length_vector(ab)
        if not Lab:
            return
        for index, vertex in enumerate(self.vertex_xyz):
            c = self.vertex_xyz[vertex]
            D = length_vector(cross_vectors(subtract_vectors(a, c), subtract_vectors(b, c)))
            if D / Lab < self.tol:
                point = Point3d(*c)
                draw_dot(point, str(index), self.dotcolor, self.textcolor)
                lines = List[Line](len(self.vertex_nbr[vertex]))
                for u, v in self.vertex_nbr[vertex]:
                    lines.Add(Line(Point3d(* self.vertex_xyz[u]), Point3d(* self.vertex_xyz[v])))
                draw_arrows(lines, self.linecolor)
                break


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
