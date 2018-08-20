"""
********************************************************************************
compas_rhino.conduits
********************************************************************************

.. currentmodule:: compas_rhino.conduits


Definition of display conduits.


.. autosummary::
    :toctree: generated/

    FacesConduit
    LabelsConduit
    LinesConduit
    PointsConduit

"""

from __future__ import print_function
from __future__ import absolute_import

from contextlib import contextmanager

import compas

try:
    import Rhino
    import scriptcontext as sc
    from Rhino.Display import DisplayConduit

except ImportError:
    compas.raise_if_ironpython()

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

    def redraw(self, k=0):
        if k % self.refreshrate == 0:
            sc.doc.Views.Redraw()
        Rhino.RhinoApp.Wait()


from .faces import *
from .labels import *
from .lines import *
from .points import *
# from .splines import *

from . import faces
from . import labels
from . import lines
from . import points
# from . import splines

__all__ = []

__all__ += faces.__all__
__all__ += labels.__all__
__all__ += lines.__all__
__all__ += points.__all__
# __all__ += splines.__all__
