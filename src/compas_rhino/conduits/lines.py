from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import System  # type: ignore

from compas.data.validators import is_sequence_of_iterable
from compas.itertools import iterable_like

from .base import BaseConduit


class LinesConduit(BaseConduit):
    """A Rhino display conduit for lines.

    Parameters
    ----------
    lines : list[[point, point] | :class:`compas.geometry.Line`]
        A list of start-end point pairs that define the lines.
    thickness : list[int], optional
        The thickness of the individual lines.
        Default is :attr:`LinesConduit.default_thickness` for all lines.
    color : list[tuple[int, int, int]], optional
        The colors of the faces.
        Default is :attr:`LinesConduit.default_color` for all lines.

    Attributes
    ----------
    color : list[System.Drawing.Color]
        A color per line.
    thickness : list[float]
        A thickness per line.

    Class Attributes
    ----------------
    default_thickness : float
        The default thickness is ``1.0``.
    default_color : System.Drawing.Color
        the default color is ``FromArgb(255, 255, 255)``.

    Examples
    --------
    .. code-block:: python

        from random import randint

        points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
        lines = [(points[i], points[i + 1]) for i in range(99)]
        conduit = LinesConduit(lines)

        with conduit.enabled():
            for i in range(100):
                points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
                conduit.lines = [(points[i], points[i + 1]) for i in range(99)]
                conduit.redraw(pause=0.1)

    """

    default_thickness = 1.0
    default_color = System.Drawing.Color.FromArgb(255, 255, 255)

    def __init__(self, lines, thickness=None, color=None, **kwargs):
        super(LinesConduit, self).__init__(**kwargs)
        self._thickness = None
        self._color = None
        self.lines = lines or []
        self.thickness = thickness
        self.color = color

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, thickness):
        thickness = thickness or self.default_thickness
        try:
            len(thickness)  # type: ignore
        except TypeError:
            thickness = [thickness]
        thickness = iterable_like(self.lines, thickness, self.default_thickness)
        self._thickness = list(thickness)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        color = color or self.default_color
        if not is_sequence_of_iterable(color):
            color = [color]
        self._color = [System.Drawing.Color.FromArgb(*c) for c in iterable_like(self.lines, color, self.default_color)]

    def DrawForeground(self, e):
        """Draw the lines.

        Parameters
        ----------
        e : Rhino.Display.DrawEventArgs

        Returns
        -------
        None

        """
        for (start, end), color, thickness in zip(self.lines, self.color, self.thickness):  # type: ignore
            e.Display.DrawLine(
                Rhino.Geometry.Point3d(*start),
                Rhino.Geometry.Point3d(*end),
                color,
                thickness,
            )
