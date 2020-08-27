from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino

from compas_rhino.objects._object import BaseObject

from compas_rhino.objects.modify import mesh_update_attributes
from compas_rhino.objects.modify import mesh_update_vertex_attributes
from compas_rhino.objects.modify import mesh_update_face_attributes
from compas_rhino.objects.modify import mesh_update_edge_attributes

from compas_rhino.objects.modify import mesh_move_vertex
from compas_rhino.objects.modify import mesh_move_vertices
from compas_rhino.objects.modify import mesh_move_face


__all__ = ['MeshObject']


class MeshObject(BaseObject):
    """Class for representing COMPAS meshes in Rhino.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh data structure.
    scene : :class:`compas.scenes.Scene`, optional
        A scene object.
    name : str, optional
        The name of the object.
    layer : str, optional
        The layer for drawing.
    visible : bool, optional
        Toggle for the visibility of the object.
    settings : dict, optional
        A dictionary of settings.

    Attributes
    ----------
    guid_vertex : dict
        Dictionary mapping Rhino object GUIDs to COMPAS mesh vertex identifiers.
    guid_face : dict
        Dictionary mapping Rhino object GUIDs to COMPAS mesh face identifiers.
    guid_edge : dict
        Dictionary mapping Rhino object GUIDs to COMPAS mesh edge identifiers.

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas_rhino.objects import MeshObject

        mesh = Mesh.from_off(compas.get('tubemesh.off'))
        meshobject = MeshObject(mesh, name='MeshObject', layer='COMPAS::MeshObject', visible=True)
        meshobject.clear()
        meshobject.clear_layer()
        meshobject.draw()
        meshobject.redraw()

        vertices = meshobject.select_vertices()
        if meshobject.modify_vertices(vertices):
            meshobject.clear()
            meshobject.draw()
            meshobject.redraw()

    """

    modify = mesh_update_attributes
    modify_vertices = mesh_update_vertex_attributes
    modify_faces = mesh_update_face_attributes
    modify_edges = mesh_update_edge_attributes

    def __init__(self, mesh, scene=None, name=None, layer=None, visible=True, settings=None):
        super(MeshObject, self).__init__(mesh, scene, name, layer, visible, settings)
        self._guid_vertex = {}
        self._guid_face = {}
        self._guid_edge = {}

    @property
    def mesh(self):
        return self.item

    @mesh.setter
    def mesh(self, mesh):
        self.item = mesh

    def clear(self):
        self.artist.clear()

    def draw(self):
        """Draw the object representing the mesh.
        """
        if not self.visible:
            return
        self.artist.draw()

    def select(self):
        raise NotImplementedError

    def select_vertices(self):
        """Select vertices of the mesh.

        Returns
        -------
        list
            A list of vertex identifiers.
        """
        guids = compas_rhino.select_points()
        vertices = [self.artist.guid_vertex[guid] for guid in guids if guid in self.artist.guid_vertex]
        return vertices

    def select_faces(self):
        """Select faces of the mesh.

        Returns
        -------
        list
            A list of face identifiers.
        """
        guids = compas_rhino.select_meshes()
        faces = [self.artist.guid_face[guid] for guid in guids if guid in self.artist.guid_face]
        return faces

    def select_edges(self):
        """Select edges of the mesh.

        Returns
        -------
        list
            A list of edge identifiers.
        """
        guids = compas_rhino.select_lines()
        edges = [self.artist.guid_edge[guid] for guid in guids if guid in self.artist.guid_edge]
        return edges

    def move(self):
        raise NotImplementedError

    def move_vertex(self, vertex):
        return mesh_move_vertex(self.mesh, vertex)

    def move_vertices(self, vertices):
        return mesh_move_vertices(self.mesh, vertices)

    def move_face(self, face):
        return mesh_move_face(self.mesh, face)


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pass
