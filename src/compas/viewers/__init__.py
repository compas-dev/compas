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
    NetworkViewer
    MeshViewer
    VolMeshViewer

"""

from compas.viewers import viewer
from compas.viewers import meshviewer
from compas.viewers import networkviewer
from compas.viewers import volmeshviewer
from compas.viewers import vtkviewer
from compas.viewers import vtkvoxels

from .core import *
from .viewer import *
from .vtkviewer import *
from .vtkvoxels import *
from .networkviewer import *
from .meshviewer import *
from .volmeshviewer import *


__all__ = [] 
__all__ += viewer.__all__
__all__ += meshviewer.__all__
__all__ += networkviewer.__all__ 
__all__ += meshviewer.__all__
__all__ += vtkviewer.__all__
