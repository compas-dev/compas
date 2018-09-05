"""
********************************************************************************
compas.viewers
********************************************************************************

.. currentmodule:: compas.viewers


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Viewer
    MeshViewer

"""
from __future__ import absolute_import

from .core import *
from .viewer import *
from .meshviewer import *

try:
    from .vtkviewer import *
except:
    pass

from . import viewer
from . import meshviewer

try:
    from . import vtkviewer
except:
    pass

__all__ = []
__all__ += viewer.__all__
__all__ += meshviewer.__all__

try:
    __all__ += vtkviewer.__all__
except:
    pass
