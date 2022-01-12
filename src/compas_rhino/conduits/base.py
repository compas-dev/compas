from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time
from contextlib import contextmanager

import Rhino
import scriptcontext as sc


class BaseConduit(Rhino.Display.DisplayConduit):
    """Base class for conduits.

    Parameters
    ----------
    refreshrate : int, optional
        The number of iterations after which the conduit should be redrawn.

    """

    def __init__(self, refreshrate=1):
        super(BaseConduit, self).__init__()
        self.refreshrate = refreshrate

    @contextmanager
    def enabled(self):
        """Create a safe context for the conduit with automatic enabling and disabling.

        Yields
        ------
        None

        Examples
        --------
        .. code-block:: python

            with conduit.enabled():
                for i in range(10):
                    conduit.redraw(k=1)

        """
        self.enable()
        try:
            yield
        except Exception as e:
            print(e)
        finally:
            self.disable()

    def CalculateBoundingBox(self, e):
        """Calculate the model extents that should be included in the visualization.

        Parameters
        ----------
        e : Rhino.DisplayCalculateBoundingBoxEventArgs

        Returns
        -------
        None

        """
        bbox = Rhino.Geometry.BoundingBox(-1000, -1000, -1000, 1000, 1000, 1000)
        e.IncludeBoundingBox(bbox)

    def enable(self):
        """Enable the conduit.

        Returns
        -------
        None

        """
        self.Enabled = True

    def disable(self):
        """Disable the conduit.

        Returns
        -------
        None

        """
        self.Enabled = False

    def redraw(self, k=0, pause=0.0):
        """Redraw the conduit.

        Parameters
        ----------
        k : int, optional
            The current iteration.
            If the current iteration is a multiple of :attr:`BaseConduit.refreshrate`, the conduit will be redrawn.
        pause : float, optional
            Include a pause after redrawing.
            The pause value should be provided in seconds.

        Returns
        -------
        None

        """
        if k % self.refreshrate == 0:
            sc.doc.Views.Redraw()
        Rhino.RhinoApp.Wait()
        if pause:
            time.sleep(pause)
