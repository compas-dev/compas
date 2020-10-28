"""
********************************************************************************
conduits
********************************************************************************

.. currentmodule:: compas_rhino.conduits

.. rst-class:: lead

Display conduits can be used to visualize iterative processes
with less of a performance penalty than with regular geometry objects.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_rhino.artists import MeshArtist
    from compas_rhino.conduits import LinesConduit

    mesh = Mesh.from_obj(compas.get('faces.obj'))
    fixed = list(mesh.vertices_where({'vertex_degree': 2})

    artist = MeshArtist(mesh, layer="COMPAS::faces.obj")
    artist.clear_layer()
    artist.draw_mesh()
    artist.redraw()

    conduit = LinesConduit()

    def redraw(k, args):
        conduit.lines = [mesh.edge_coordinates(*edges) for edge in mesh.edges()]
        conduit.redraw()

    with conduit.enabled():
        mesh.smooth_centroid(
            fixed=fixed),
            kmax=100,
            callback=redraw)


BaseConduit
===========

.. autoclass:: BaseConduit
    :members: enabled, enable, disable, redraw

----

Faces Conduit
=============

.. autoclass:: FacesConduit
    :no-show-inheritance:

----

Lines Conduit
=============

.. autoclass:: LinesConduit
    :no-show-inheritance:

----

Points Conduit
==============

.. autoclass:: PointsConduit
    :no-show-inheritance:

----

Labels Conduit
==============

.. autoclass:: LabelsConduit
    :no-show-inheritance:

"""
from __future__ import absolute_import

from .base import *  # noqa: F401 E402 F403

from .faces import *  # noqa: F401 E402 F403
from .labels import *  # noqa: F401 E402 F403
from .lines import *  # noqa: F401 E402 F403
from .points import *  # noqa: F401 E402 F403

__all__ = [name for name in dir() if not name.startswith('_')]
