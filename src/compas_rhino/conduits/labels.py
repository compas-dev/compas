from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
from compas_rhino.conduits import Conduit

try:
    from Rhino.Geometry import Point3d
    from System.Drawing.colour import FromArgb

except ImportError:
    compas.raise_if_ironpython()


__author__     = 'Tom Van Mele'
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['LabelsConduit', ]


class LabelsConduit(Conduit):
    """A Rhino display conduit for labels.

    Parameters
    ----------
    labels : list of 2-tuple
        A list of label tuples.
        Each tuple contains a position and text for the label.
    colour : list of 2-tuple, optional
        The colours of the labels.
        Each colour is a tuple with a background colour and a text colour.
        Default is ``((0, 0, 0), (255, 255, 255))`` for all labels.

    Attributes
    ----------
    colour
    labels : list
        A list of label tuples.
        Each tuple contains a position and text for the label.

    Example
    -------
    .. code-block:: python

        from random import randint
        import time
        from compas_rhino.conduits import LabelsConduit

        labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]

        try:
            conduit = LabelsConduit(labels)
            conduit.enable()

            for i in range(100):
                labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]
                conduit.labels = labels
                conduit.redraw()
                time.sleep(0.1)

        except Exception as e:
            print e

        finally:
            conduit.disable()
            del conduit

    """
    def __init__(self, labels, colour=None, **kwargs):
        super(LabelsConduit, self).__init__(**kwargs)
        self._default_colour = FromArgb(0, 0, 0)
        self._default_textcolour = FromArgb(255, 255, 255)
        self._colour = None
        self.labels = labels or []
        self.colour = colour

    @property
    def colour(self):
        """list : Individual label colours.

        Parameters
        ----------
        colour : list of str or 3-tuple
            The specification of background and text colour of each face in hex or RGB(255) format.

        """
        return self._colours
    
    @colour.setter
    def colour(self, colour):
        if colour:
            colour[:] = [(FromArgb(* colour_to_rgb(bgc)), FromArgb(* colour_to_rgb(tc))) for bgc, tc in colour]
            l = len(self.labels)
            c = len(colour)
            if c < l:
                colours += [(self._default_colour, self._default_textcolour) for i in range(l - c)]
            elif c > l:
                colour[:] = colour[:l]
            self._colour = colour

    def DrawForeground(self, e):
        for i, (pos, text) in enumerate(self.labels):
            if self.colour:
                colour, textcolour = self.colour[i]
                e.Display.DrawDot(Point3d(*pos), text, colour, textcolour)
            else:
                e.Display.DrawDot(Point3d(*pos), text, self._default_colour, self._default_textcolour)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from random import randint
    import time

    labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]

    try:
        conduit = LabelsConduit(labels)
        conduit.enable()

        for i in range(100):
            labels = [([1.0 * randint(0, 100), 1.0 * randint(0, 100), 0.0], str(i)) for i in range(100)]
            conduit.labels = labels
            conduit.redraw()
            time.sleep(0.1)

    except Exception as e:
        print(e)

    finally:
        conduit.disable()
        del conduit
