from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

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
    """"""

    def __init__(self, mesh, tol=0.1, dotcolor=None, textcolor=None, linecolor=None, **kwargs):
        super(MeshVertexInspector, self).__init__(**kwargs)
        self.mesh = mesh
        self.tol = tol
        dotcolor = dotcolor or (255, 255, 0)
        textcolor = textcolor or (0, 0, 0)
        linecolor = linecolor or (255, 255, 0)
        self.dotcolor = FromArgb(*dotcolor)
        self.textcolor = FromArgb(*textcolor)
        self.linecolor = FromArgb(*linecolor)
        self.mouse = Mouse(self)
        self.vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        self.vertex_nbr = {vertex: mesh.vertex_neighbors(vertex) for vertex in mesh.vertices()}

    def enable(self):
        self.mouse.Enabled = True
        self.Enabled = True

    def disable(self):
        self.mouse.Enabled = False
        self.Enabled = False

    def DrawForeground(self, e):
        draw_dot = e.Display.DrawDot
        draw_arrow = e.Display.DrawArrow
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
                for nbr in self.vertex_nbr[vertex]:
                    draw_arrow(Line(point, Point3d(* self.vertex_xyz[nbr])), self.dotcolor)
                break


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
