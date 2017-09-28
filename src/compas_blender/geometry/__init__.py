"""
.. _compas_blender.geometry:

********************************************************************************
geometry
********************************************************************************

.. module:: compas_blender.geometry


curve
-----

.. autosummary::
    :toctree: generated/


mesh
----

.. autosummary::
    :toctree: generated/


point
-----

.. autosummary::
    :toctree: generated/


surface
-------

.. autosummary::
    :toctree: generated/



"""

from .curve import *
from .mesh import *
from .point import *
from .surface import *

from .curve import __all__ as a
from .mesh import __all__ as b
from .point import __all__ as c
from .surface import __all__ as d

__all__ = a + b + c + d
