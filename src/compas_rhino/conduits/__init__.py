"""
********************************************************************************
conduits
********************************************************************************

.. module:: compas_rhino.conduits


Definition of display conduits.


.. autosummary::
    :toctree: generated/

    FacesConduit
    LabelsConduit
    LinesConduit
    MeshConduit
    PointsConduit
    SplinesConduit

"""

from __future__ import print_function

from contextlib import contextmanager

try:
    import Rhino
    import scriptcontext as sc
    from Rhino.Display import DisplayConduit

except ImportError:
    import sys
    if 'ironpython' in sys.version.lower():
        raise

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
from .mesh import *
from .points import *
from .splines import *

from .faces import __all__ as a
from .labels import __all__ as b
from .lines import __all__ as c
from .mesh import __all__ as d
from .points import __all__ as f
from .splines import __all__ as g

__all__ = a + b + c + d + f + g
