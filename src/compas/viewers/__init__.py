""".. _compas.viewers:

********************************************************************************
viewers
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

from .core import *
from .viewer import *
from .networkviewer import *
from .meshviewer import *
from .volmeshviewer import *


from .viewer import __all__ as b
from .networkviewer import __all__ as c
from .meshviewer import __all__ as d
from .volmeshviewer import __all__ as e

__all__ = b + c + d + e
