from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time
from contextlib import contextmanager

import Rhino
import scriptcontext as sc


__all__ = ['BaseConduit']


class BaseConduit(Rhino.Display.DisplayConduit):
    """Base class for conduits.

    Parameters
    ----------
    refreshrate : int, optional
        The number of iterations after which the conduit should be redrawn.
        Default is ``1``.
    """

    def __init__(self, refreshrate=1):
        super(BaseConduit, self).__init__()
        self.refreshrate = refreshrate

    @contextmanager
    def enabled(self):
        self.enable()
        try:
            yield
        except Exception as e:
            print(e)
        finally:
            self.disable()

    def enable(self):
        """Enable the conduit."""
        self.Enabled = True

    def disable(self):
        """Disable the conduit."""
        self.Enabled = False

    def redraw(self, k=0, pause=None):
        """Redraw the conduit.

        Parameters
        ----------
        k : int, optional
            The current iteration.
            If the current iteration is a multiple of ``refreshrate``, the conduit will be redrawn.
            Default is ``0``.
        pause : float, optional
            Include a pause after redrawing.
            The pause value should be provided in seconds.
            Default is no pause.
        """
        if k % self.refreshrate == 0:
            sc.doc.Views.Redraw()
        Rhino.RhinoApp.Wait()
        if pause:
            time.sleep(pause)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
