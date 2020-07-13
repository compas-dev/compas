"""
********************************************************************************
conduits
********************************************************************************

.. currentmodule:: compas_rhino.conduits


Definition of display conduits.


Base Classes
============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Conduit


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshConduit
    FacesConduit
    LinesConduit
    PointsConduit
    LabelsConduit

"""
from __future__ import absolute_import

import time
from contextlib import contextmanager

import compas

if compas.RHINO:
    import Rhino
    import scriptcontext as sc


class Conduit(Rhino.Display.DisplayConduit):
    """Base class for conduits.

    Parameters
    ----------
    refreshrate : int, optional
        The number of iterations after which the conduit should be redrawn.
        Default is ``1``.
    """

    def __init__(self, refreshrate=1):
        super(Conduit, self).__init__()
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


from .mesh import *  # noqa: F401 E402 F403
from .faces import *  # noqa: F401 E402 F403
from .labels import *  # noqa: F401 E402 F403
from .lines import *  # noqa: F401 E402 F403
from .points import *  # noqa: F401 E402 F403

__all__ = [name for name in dir() if not name.startswith('_')]
