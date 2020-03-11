from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_rhino.conduits import Conduit
from compas.utilities import color_to_rgb

try:
    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Line

    from System.Collections.Generic import List
    from System.Drawing.Color import FromArgb

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['MeshConduit']


class MeshConduit(Conduit):
    """A Rhino display conduit for meshes.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A COMPAS mesh.
    thickness : list of int, optional
        The thickness of the lines of the wireframe.
        Default is ``1.0`` for all lines.
    color : list of str or 3-tuple, optional
        The colors of the lines.
        Default is ``(255, 255, 255)`` for all lines.

    Attributes
    ----------
    color
    thickness

    Example
    -------
    .. code-block:: python

        pass

    """
    def __init__(self, mesh, thickness=None, color=None, **kwargs):
        super(MeshConduit, self).__init__(**kwargs)
        self._default_thickness = 1.0
        self._default_color = FromArgb(255, 255, 255)
        self._thickness = None
        self._color = None
        self.mesh = mesh
        self.thickness = thickness
        self.color = color

    @property
    def lines(self):
        key_point = {key: Point3d(attr['x'], attr['y'], attr['z']) for key, attr in self.mesh.vertices(True)}
        for i, (u, v) in enumerate(self.mesh.edges()):
            yield i, key_point[u], key_point[v]

    @property
    def thickness(self):
        """list : Individual line thicknesses.

        Parameters
        ----------
        thickness : list of int
            The thickness of each line.

        """
        return self._thickness

    @thickness.setter
    def thickness(self, thickness):
        if thickness:
            e = self.mesh.number_of_edges()
            t = len(thickness)
            if t < e:
                thickness += [self._default_thickness for i in range(e - t)]
            elif t > e:
                thickness[:] = thickness[:e]
            self._thickness = thickness

    @property
    def color(self):
        """list : Individual line colors.

        Parameters
        ----------
        color : list of str or 3-tuple
            The color specification of each line in hex or RGB(255) format.

        """
        return self._color

    @color.setter
    def color(self, color):
        if color:
            color[:] = [FromArgb(* color_to_rgb(c)) for c in color]
            e = self.mesh.number_of_edges()
            c = len(color)
            if c < e:
                color += [self._default_color for i in range(e - c)]
            elif c > e:
                color[:] = color[:e]
            self._color = color

    def DrawForeground(self, e):
        draw_line = e.Display.DrawLine
        draw_lines = e.Display.DrawLines

        if self.color:
            if self.thickness:
                for i, start, end in self.lines:
                    draw_line(start, end, self.color[i], self.thickness[i])
            else:
                for i, start, end in self.lines:
                    draw_line(start, end, self.color[i], self._default_thickness)

        elif self.thickness:
            if self.color:
                for i, start, end in self.lines:
                    draw_line(start, end, self.color[i], self.thickness[i])
            else:
                for i, start, end in self.lines:
                    draw_line(start, end, self._default_color, self.thickness[i])

        else:
            lines = List[Line](self.mesh.number_of_edges())
            for i, start, end in self.lines:
                lines.Add(Line(start, end))
            draw_lines(lines, self._default_color, self._default_thickness)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
