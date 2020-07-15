"""
********************************************************************************
geometry
********************************************************************************

.. currentmodule:: compas_rhino.geometry

.. rst-class:: lead

Wrappers for Rhino objects that can be used to convert Rhino geometry and data to COMPAS objects.

.. code-block:: python

    import compas_rhino
    from compas_rhino.geometry import RhinoMesh

    guid = compas_rhino.select_mesh()
    mesh = RhinoMesh.from_guid(guid).to_compas()

----

BaseRhinoGeometry
=================

.. autoclass:: BaseRhinoGeometry

----

RhinoPoint
==========

.. autoclass:: RhinoPoint

RhinoVector
===========

.. autoclass:: RhinoVector

RhinoLine
=========

.. autoclass:: RhinoLine

RhinoPlane
==========

.. autoclass:: RhinoPlane

RhinoMesh
=========

.. autoclass:: RhinoMesh

RhinoCurve
==========

.. autoclass:: RhinoCurve

RhinoSurface
============

.. autoclass:: RhinoSurface

"""
from __future__ import absolute_import

from .base import *  # noqa: F401 F403

from .curve import *  # noqa: F401 F403
from .line import *  # noqa: F401 F403
from .mesh import *  # noqa: F401 F403
from .plane import *  # noqa: F401 F403
from .point import *  # noqa: F401 F403
from .surface import *  # noqa: F401 F403
from .vector import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
