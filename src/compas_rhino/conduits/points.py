from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import System  # type: ignore

from compas.data.validators import is_sequence_of_iterable
from compas.itertools import iterable_like

from .base import BaseConduit


class PointsConduit(BaseConduit):
    """A Rhino display conduit for points.

    Parameters
    ----------
    points : list[[float, float, float] | :class:`compas.geometry.Point`]
        The coordinates of the points.
    size : list[int], optional
        The size of the points.
        Default is :attr:`PointsConduit.default_size` for all points.
    color : list[tuple[int, int, int]]
        The individual colors of the points.
        Default is :attr:`PointsConduit.default_color` for all points.

    Attributes
    ----------
    size : list[float]
        The size specification per point.
    color : list[System.Drawing.Color]
        The color per point.

    Class Attributes
    ----------------
    default_size : float
        The default size is ``3``.
    default_color : System.Drawing.Color
        The default color is ``FromArgb(255, 0, 0)``.

    Examples
    --------
    .. code-block:: python

        from random import randint
        from compas_rhino.conduits import PointsConduit

        points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
        conduit = PointsConduit(points)

        with conduit.enabled():
            for i in range(100):
                conduit.points = [(1.0 * randint(0, 30), 1.0 * randint(0, 30), 0.0) for _ in range(100)]
                conduit.redraw(pause=0.1)

    """

    default_size = 3
    default_color = System.Drawing.Color.FromArgb(255, 0, 0)

    def __init__(self, points, size=None, color=None, **kwargs):
        super(PointsConduit, self).__init__(**kwargs)
        self._size = None
        self._color = None
        self.points = points or []
        self.size = size
        self.color = color

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        size = size or self.default_size
        try:
            len(size)  # type: ignore
        except TypeError:
            size = [size]
        size = iterable_like(self.points, size, self.default_size)
        self._size = list(size)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        color = color or self.default_color
        if not is_sequence_of_iterable(color):
            color = [color]
        color = [System.Drawing.Color.FromArgb(*c) for c in iterable_like(self.points, color, self.default_color)]
        self._color = color

    def DrawForeground(self, e):
        """Draw the points.

        Parameters
        ----------
        e : Rhino.Display.DrawEventArgs

        Returns
        -------
        None

        """
        for xyz, size, color in zip(self.points, self.size, self.color):  # type: ignore
            e.Display.DrawPoint(Rhino.Geometry.Point3d(*xyz), Rhino.Display.PointStyle.Simple, size, color)
