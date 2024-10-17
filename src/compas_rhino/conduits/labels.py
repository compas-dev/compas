from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino  # type: ignore
import System  # type: ignore

from compas.data.validators import is_sequence_of_iterable
from compas.itertools import iterable_like

from .base import BaseConduit


class LabelsConduit(BaseConduit):
    """A Rhino display conduit for labels.

    Parameters
    ----------
    labels : list[tuple[[float, float, float] | :class:`compas.geometry.Point`, str]]
        A list of label tuples.
        Each tuple contains a position and text for the label.
    color : list[tuple[tuple[int, int, int], tuple[int, int, int]]], optional
        The colors of the labels.
        Each color is a tuple with a background color and a text color.
        The default background color is :attr:`LabelsConduit.default_color`,
        and the default text color is :attr:`LabelsConduit.default_textcolor`.

    Attributes
    ----------
    color : list[tuple[System.Drawing.Color, System.Drawing.Color]]
        A color specification per label.
    labels : list[tuple[[float, float, float] | :class:`compas.geometry.Point`, str]]
        A list of label tuples.
        Each tuple contains a position and text for the label.

    Class Attributes
    ----------------
    default_color : System.Drawing.Color
        The default background color is ``FromArgb(0, 0, 0)``.
    default_textcolor : System.Drawing.Color
        The default text color is ``FromArgb(255, 255, 255)``.

    Examples
    --------
    .. code-block:: python

        from random import randint
        from compas_rhino.conduits import LabelsConduit

        labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]

        conduit = LabelsConduit(labels)

        with conduit.enabled():
            for i in range(100):
                conduit.labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]
                conduit.redraw(pause=0.1)

    """

    default_color = System.Drawing.Color.FromArgb(0, 0, 0)
    default_textcolor = System.Drawing.Color.FromArgb(255, 255, 255)

    def __init__(self, labels, color=None, **kwargs):
        super(LabelsConduit, self).__init__(**kwargs)
        self._color = None
        self.labels = labels or []
        self.color = color

    @property
    def color(self):
        return self._colors

    @color.setter
    def color(self, color):
        if not color:
            return
        if not is_sequence_of_iterable(color[0]):
            # the first item in the list should be a tuple of colors
            # if not, wrap the tuple
            color = [color]
        color = [
            (System.Drawing.Color.FromArgb(*bg), System.Drawing.Color.FromArgb(*text))
            for bg, text in iterable_like(self.labels, color, (self.default_color, self.default_textcolor))  # type: ignore
        ]
        self._color = color

    def DrawForeground(self, e):
        """Draw the labels as text dots.

        Parameters
        ----------
        e : Rhino.Display.DrawEventArgs

        Returns
        -------
        None

        """
        for i, (pos, text) in enumerate(self.labels):
            if self.color:
                color, textcolor = self.color[i]
                e.Display.DrawDot(Rhino.Geometry.Point3d(*pos), text, color, textcolor)
            else:
                e.Display.DrawDot(Rhino.Geometry.Point3d(*pos), text, self.default_color, self.default_textcolor)
