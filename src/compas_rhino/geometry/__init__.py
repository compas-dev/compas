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

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    BaseRhinoGeometry
    RhinoBox
    RhinoCircle
    RhinoCurve
    RhinoEllipse
    RhinoLine
    RhinoMesh
    RhinoPlane
    RhinoPoint
    RhinoPolyline
    RhinoSphere
    RhinoSurface
    RhinoVector

"""
from __future__ import absolute_import

from ._geometry import BaseRhinoGeometry

from .box import RhinoBox
from .circle import RhinoCircle
from .curve import RhinoCurve
from .ellipse import RhinoEllipse
from .line import RhinoLine
from .mesh import RhinoMesh
from .plane import RhinoPlane
from .point import RhinoPoint
from .polyline import RhinoPolyline
from .sphere import RhinoSphere
from .surface import RhinoSurface
from .vector import RhinoVector

__all__ = [
    'BaseRhinoGeometry',
    'RhinoBox',
    'RhinoCircle',
    'RhinoCurve',
    'RhinoEllipse',
    'RhinoLine',
    'RhinoMesh',
    'RhinoPlane',
    'RhinoPoint',
    'RhinoPolyline',
    'RhinoSphere',
    'RhinoSurface',
    'RhinoVector',
]
