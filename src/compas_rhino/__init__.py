"""
********************************************************************************
compas_rhino
********************************************************************************

.. module:: compas_rhino


.. toctree::
    :maxdepth: 1

    compas_rhino.forms
    compas_rhino.geometry
    compas_rhino.helpers
    compas_rhino.ui
    compas_rhino.utilities

"""

from .utilities import *
from .utilities import __all__ as a

from .helpers import *
from .helpers import __all__ as b

__version__ = '0.1.0'
__all__ = a + b + ['__version__']
