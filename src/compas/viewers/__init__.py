""".. _compas.viewers:

********************************************************************************
viewers
********************************************************************************

.. module:: compas.viewers

.. note::

    The viewers package is built around PyOpenGL and PySide(2).

    * PyOpenGL: http://pyopengl.sourceforge.net/
    * PySide: http://pyside.github.io/docs/pyside/index.html


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
