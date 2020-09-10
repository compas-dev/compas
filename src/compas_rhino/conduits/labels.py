from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from System.Drawing.Color import FromArgb
from Rhino.Geometry import Point3d

from compas_rhino.conduits.base import BaseConduit
from compas.utilities import color_to_rgb


__all__ = ['LabelsConduit']


class LabelsConduit(BaseConduit):
    """A Rhino display conduit for labels.

    Parameters
    ----------
    labels : list of 2-tuple
        A list of label tuples.
        Each tuple contains a position and text for the label.
    color : list of 2-tuple, optional
        The colors of the labels.
        Each color is a tuple with a background color and a text color.
        Default is ``((0, 0, 0), (255, 255, 255))`` for all labels.

    Attributes
    ----------
    color : list of RGB colors
        A color specification per label.
    labels : list
        A list of label tuples.
        Each tuple contains a position and text for the label.

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
    def __init__(self, labels, color=None, **kwargs):
        super(LabelsConduit, self).__init__(**kwargs)
        self._default_color = FromArgb(0, 0, 0)
        self._default_textcolor = FromArgb(255, 255, 255)
        self._color = None
        self.labels = labels or []
        self.color = color

    @property
    def color(self):
        return self._colors

    @color.setter
    def color(self, color):
        if color:
            color[:] = [(FromArgb(* color_to_rgb(bgc)), FromArgb(* color_to_rgb(tc))) for bgc, tc in color]
            l = len(self.labels)  # noqa: E741
            c = len(color)
            if c < l:
                color += [(self._default_color, self._default_textcolor) for i in range(l - c)]
            elif c > l:
                color[:] = color[:l]
            self._color = color

    def DrawForeground(self, e):
        for i, (pos, text) in enumerate(self.labels):
            if self.color:
                color, textcolor = self.color[i]
                e.Display.DrawDot(Point3d(*pos), text, color, textcolor)
            else:
                e.Display.DrawDot(Point3d(*pos), text, self._default_color, self._default_textcolor)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
