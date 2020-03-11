"""
********************************************************************************
compas_rhino.conduits
********************************************************************************

.. currentmodule:: compas_rhino.conduits


Definition of display conduits.


.. autosummary::
    :toctree: generated/
    :nosignatures:

    MeshConduit
    FacesConduit
    LinesConduit
    PointsConduit
    LabelsConduit

"""

from __future__ import print_function
from __future__ import absolute_import

import time
from contextlib import contextmanager

import compas

if compas.IPY:
    import Rhino
    import scriptcontext as sc
    from Rhino.Display import DisplayConduit
else:
    class DisplayConduit(object):
        pass


class Conduit(DisplayConduit):

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
        self.Enabled = True

    def disable(self):
        self.Enabled = False

    def redraw(self, k=0, pause=None):
        if k % self.refreshrate == 0:
            sc.doc.Views.Redraw()
        Rhino.RhinoApp.Wait()
        if pause:
            time.sleep(pause)


from .mesh import *  # noqa: F401 F403
from .faces import *  # noqa: F401 F403
from .labels import *  # noqa: F401 F403
from .lines import *  # noqa: F401 F403
from .points import *  # noqa: F401 F403
# from .splines import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
