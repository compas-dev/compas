"""
.. compas_compas_rhino.conduits:

********************************************************************************
conduits
********************************************************************************

.. module:: compas_compas_rhino.conduits


Definition of display conduits.


.. autosummary::
    :toctree: generated/

    FacesConduit
    LabelsConduit
    LinesConduit
    MeshConduit
    PointPairsConduit
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
    import platform
    if platform.python_implementation() == 'IronPython':
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
from .pointpairs import *
from .points import *
from .splines import *
