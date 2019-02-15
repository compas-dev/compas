"""
********************************************************************************
compas_rhino.modifiers
********************************************************************************

.. currentmodule:: compas_rhino.modifiers

.. autosummary::
    :toctree: generated/
    :nosignatures:

    EdgeModifier
    FaceModifier
    VertexModifier


`Modifiers` define static methods for modifying the geometry or data attributes of
elements of COMPAS data structures and of the data structures themselves.

All static methods take as first parameter a data structure instance.
As a consequence the methods can be used directly from the class (without making an instance)
or they can be added to (sub-classes of) the data structures themselves to extend
their functionality in Rhino.


.. code-block:: python

    import compas

    from compas.datastructures import Mesh

    from compas_rhino.artists import MeshArtist

    from compas_rhino.modifiers import VertexModifier
    from compas_rhino.selectors import VertexSelector

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    artist = MeshArtist(mesh, layer='Mesh')
    artist.clear_layer()
    artist.draw_vertices()
    artist.draw_edges()
    artist.redraw()

    keys = VertexSelector.select_vertices(mesh)

    if keys:
        if VertexModifier.update_vertex_attributes(mesh, keys):
            artist.clear_layer()
            artist.draw_vertices()
            artist.draw_edges()
            artist.redraw()


.. code-block:: python

    import compas

    from compas.datastructures import Mesh

    from compas_rhino.artists import MeshArtist

    from compas_rhino.modifiers import VertexModifier
    from compas_rhino.selectors import VertexSelector


    class CustomMesh(VertexSelector, VertexModifier, Mesh):

        def draw(self):
            artist = MeshArtist(self, layer='Mesh')
            artist.clear_layer()
            artist.draw_vertices()
            artist.draw_edges()
            artist.redraw()


    mesh = CustomMesh.from_obj(compas.get('faces.obj'))
    mesh.draw()

    keys = mesh.select_vertices()

    if keys:
        if mesh.update_vertex_attributes(keys):
            mesh.draw()


"""
from __future__ import absolute_import


from .vertexmodifier import *
from .edgemodifier import *
from .facemodifier import *

from .modifier import *


__all__ = [name for name in dir() if not name.startswith('_')]
