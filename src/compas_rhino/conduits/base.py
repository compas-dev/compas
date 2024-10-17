from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
from contextlib import contextmanager

import Rhino  # type: ignore
import scriptcontext as sc  # type: ignore


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
        """Create a context for the conduit with automatic enabling and disabling.

        Yields
        ------
        None

        Notes
        -----
        The conduit is automatically enabled when the context is entered,
        and is guaranteed to be disabled when the context is exited,
        even when an error occurs during the execution of the code in the context.

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

        Raises
        ------
        ValueError
            If `pause` is not a positive number.

        """
        if pause < 0:
            raise ValueError("The value of pause should be a positive number.")

        if k % self.refreshrate == 0:
            sc.doc.Views.Redraw()
        Rhino.RhinoApp.Wait()
        if pause:
            time.sleep(pause)
