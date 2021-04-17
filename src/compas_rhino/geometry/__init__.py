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


BaseRhinoGeometry
=================

.. autoclass:: BaseRhinoGeometry
    :members: from_geometry, from_selection, to_compas, from_guid, from_object, transform

----

RhinoPoint
==========

.. autoclass:: RhinoPoint
    :members: from_geometry, from_selection, to_compas
    :no-show-inheritance:

----

RhinoVector
===========

.. autoclass:: RhinoVector
    :members: from_geometry, from_selection, to_compas
    :no-show-inheritance:

----

RhinoLine
=========

.. autoclass:: RhinoLine
    :members: from_geometry, from_selection, to_compas
    :no-show-inheritance:

----

RhinoPlane
==========

.. autoclass:: RhinoPlane
    :members: from_geometry, from_selection, to_compas
    :no-show-inheritance:

----

RhinoMesh
=========

.. autoclass:: RhinoMesh
    :members: from_geometry, from_selection, to_compas
    :no-show-inheritance:

----

RhinoCurve
==========

.. autoclass:: RhinoCurve
    :members: from_geometry, from_selection, to_compas
    :no-show-inheritance:

----

RhinoSurface
============

.. autoclass:: RhinoSurface
    :members: from_geometry, from_selection, to_compas
    :no-show-inheritance:

"""
from __future__ import absolute_import

from ._geometry import BaseRhinoGeometry

from .curve import RhinoCurve
from .line import RhinoLine
from .mesh import RhinoMesh
from .plane import RhinoPlane
from .point import RhinoPoint
from .surface import RhinoSurface
from .vector import RhinoVector

__all__ = [
    'BaseRhinoGeometry',
    'RhinoCurve',
    'RhinoLine',
    'RhinoMesh',
    'RhinoPlane',
    'RhinoPoint',
    'RhinoSurface',
    'RhinoVector'
]
