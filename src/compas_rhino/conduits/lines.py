from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas.utilities import color_to_rgb
from compas_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from Rhino.Geometry import Line

    from System.Collections.Generic import List
    from System.Drawing.Color import FromArgb

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['LinesConduit']


class LinesConduit(Conduit):
    """A Rhino display conduit for lines.

    Parameters
    ----------
    lines : list of 2-tuple
        A list of start-end point pairs that define the lines.
    thickness : list of int, optional
        The thickness of the individual lines.
        Default is ``1.0`` for all lines.
    color : list of str or 3-tuple, optional
        The colors of the faces.
        Default is ``(255, 255, 255)`` for all lines.

    Attributes
    ----------
    color
    thickness
    lines : list
        A list of start-end point pairs that define the lines.

    Example
    -------
    .. code-block:: python

        from random import randint

        points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
        lines  = [(points[i], points[i + 1]) for i in range(99)]

        conduit = LinesConduit(lines)

        with conduit.enabled():
            for i in range(100):
                points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
                conduit.lines = [(points[i], points[i + 1]) for i in range(99)]
                conduit.redraw(pause=0.1)

    """
    def __init__(self, lines, thickness=None, color=None, **kwargs):
        super(LinesConduit, self).__init__(**kwargs)
        self._default_thickness = 1.0
        self._default_color = FromArgb(255, 255, 255)
        self._thickness = None
        self._color = None
        self.lines = lines or []
        self.thickness = thickness
        self.color = color

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
            try:
                len(thickness)
            except TypeError:
                thickness = [thickness]
            l = len(self.lines)
            t = len(thickness)
            if t < l:
                thickness += [self._default_thickness for i in range(l - t)]
            elif t > l:
                thickness[:] = thickness[:l]
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
            l = len(self.lines)
            if isinstance(color, (basestring, tuple)):
                # if a single color was provided
                color = [color for _ in range(l)]
            # convert the specified colors to windows system colors
            color[:] = [FromArgb(* color_to_rgb(c)) for c in color]
            c = len(color)
            if c < l:
                # pad the list with default colors
                color += [self._default_color for i in range(l - c)]
            elif c > l:
                # resize to the number of lines
                color[:] = color[:l]
            # assign to the protected attribute
            self._color = color

    def DrawForeground(self, e):
        try:
            if self.color:
                draw = e.Display.DrawLine
                if self.thickness:
                    for i, (start, end) in enumerate(self.lines):
                        draw(Point3d(*start), Point3d(*end), self.color[i], self.thickness[i])
                else:
                    for i, (start, end) in enumerate(self.lines):
                        draw(Point3d(*start), Point3d(*end), self.color[i], self._default_thickness)

            elif self.thickness:
                draw = e.Display.DrawLine
                if self.color:
                    for i, (start, end) in enumerate(self.lines):
                        draw(Point3d(*start), Point3d(*end), self.color[i], self.thickness[i])
                else:
                    for i, (start, end) in enumerate(self.lines):
                        draw(Point3d(*start), Point3d(*end), self._default_color, self.thickness[i])

            else:
                lines = List[Line](len(self.lines))
                for start, end in self.lines:
                    lines.Add(Line(Point3d(*start), Point3d(*end)))
                e.Display.DrawLines(lines, self._default_color, self._default_thickness)
        except Exception as e:
            print(e)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from random import randint

    points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
    lines  = [(points[i], points[i + 1]) for i in range(99)]

    conduit = LinesConduit(lines, color=['#ff00ff', '#ff0000'], thickness=[1, 2, 3, 4, 5, 20])

    with conduit.enabled():
        for i in range(100):
            points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
            conduit.lines = [(points[i], points[i + 1]) for i in range(99)]
            conduit.redraw(pause=0.1)
