"""
********************************************************************************
compas.viewers
********************************************************************************

.. module:: compas.viewers

This package wraps `PyOpenGL`_ and `PySide`_ to provide three-dimensional
viewers with basic visualization and user interaction capabilities.

.. _PyOpenGL: http://pyopengl.sourceforge.net
.. _PySide: http://pyside.github.io/docs/pyside/index.html


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Viewer
    MeshViewer

"""

from compas.viewers import viewer
from compas.viewers import meshviewer

try:
    from compas.viewers import vtkviewer
except:
    pass

from .core import *
from .viewer import *
from .meshviewer import *

try:
    from .vtkviewer import *
except:
    pass

__all__ = []
__all__ += viewer.__all__
__all__ += meshviewer.__all__

try:
    __all__ += vtkviewer.__all__
except:
    pass
