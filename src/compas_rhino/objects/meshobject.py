from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino
from compas_rhino.objects.base import BaseObject
from compas_rhino.objects.modifiers import VertexModifier
from compas_rhino.objects.modifiers import FaceModifier
from compas_rhino.objects.modifiers import EdgeModifier


__all__ = ['MeshObject']


class MeshObject(BaseObject):
    """Base class for COMPAS Rhino objects.

    Parameters
    ----------
    scene : :class:`compas.scenes.Scene`
        A scene object.
    mesh : :class:`compas.datastructures.Mesh`
        A mesh object.

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
        meshobject = MeshObject(None, mesh, 'MeshObject', 'COMPAS::MeshObject', True)
        meshobject.draw()
        meshobject.redraw()

        vertices = meshobject.select_vertices()

        if meshobject.modify_vertices(vertices):
            meshobject.draw()
            meshobject.redraw()

    """

    def __init__(self, scene, mesh, name=None, layer=None, visible=True, settings=None):
        super(MeshObject, self).__init__(scene, mesh, name, layer, visible)
        self._guid_vertex = {}
        self._guid_face = {}
        self._guid_edge = {}
        self.settings = settings

    @property
    def mesh(self):
        return self.item

    @mesh.setter
    def mesh(self, mesh):
        self.item = mesh

    @property
    def guid_vertex(self):
        if not self._guid_vertex:
            self._guid_vertex = {}
        return self._guid_vertex

    @guid_vertex.setter
    def guid_vertex(self, values):
        self._guid_vertex = dict(values)

    @property
    def guid_face(self):
        if not self._guid_face:
            self._guid_face = {}
        return self._guid_face

    @guid_face.setter
    def guid_face(self, values):
        self._guid_face = dict(values)

    @property
    def guid_edge(self):
        if not self._guid_edge:
            self._guid_edge = {}
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    def clear(self):
        guids_vertices = list(self.guid_vertex.keys())
        guids_faces = list(self.guid_face.keys())
        guids_edges = list(self.guid_edge.keys())
        guids = guids_vertices + guids_faces + guids_edges
        compas_rhino.delete_objects(guids, purge=True)
        self._guid_vertex = {}
        self._guid_face = {}
        self._guid_edge = {}

    def draw(self, clear_layer=True, redraw=False):
        """Draw the object representing the mesh.

        Parameters
        ----------
        clear_layer : bool, optional
            Clear the layer of the object.
            Default is ``True``.
        redraw : bool, optional
            Redraw the Rhino view.
            Default is ``False``.
        """
        self.clear()
        if clear_layer:
            self.clear_layer()
        if not self.visible:
            return
        # vertices
        if self.settings.get('show.vertices'):
            vertices = list(self.mesh.vertices())
            guids = self.artist.draw_vertices(vertices)
            self.guid_vertex = zip(guids, vertices)
        # faces
        if self.settings.get('show.faces'):
            faces = list(self.mesh.faces())
            guids = self.artist.draw_faces(faces, join_faces=True)
            self.guid_face = zip(guids, faces)
        # edges
        if self.settings.get('show.edges'):
            edges = list(self.mesh.edges())
            guids = self.artist.draw_edges(edges)
            self.guid_edge = zip(guids, edges)
        # redraw the scene
        if redraw:
            self.redraw()

    def select(self):
        pass

    def select_vertices(self):
        """Select vertices of the mesh.

        Returns
        -------
        list
            A list of vertex identifiers.
        """
        guids = compas_rhino.select_points()
        vertices = [self.guid_vertex[guid] for guid in guids if guid in self.guid_vertex]
        return vertices

    def select_faces(self):
        """Select faces of the mesh.

        Returns
        -------
        list
            A list of face identifiers.

        Notes
        -----
        This is only possible if the mesh was drawn with individual, unjoined faces.

        """
        guids = compas_rhino.select_meshes()
        faces = [self.guid_face[guid] for guid in guids if guid in self.guid_face]
        return faces

    def select_edges(self):
        """Select edges of the mesh.

        Returns
        -------
        list
            A list of edge identifiers.
        """
        guids = compas_rhino.select_lines()
        edges = [self.guid_edge[guid] for guid in guids if guid in self.guid_edge]
        return edges

    def modify(self):
        raise NotImplementedError

    def modify_vertices(self, vertices):
        """Modify the attributes of the vertices of the mesh item.

        Parameters
        ----------
        vertices : list
            The identifiers of the vertices of which the attributes will be updated.

        Returns
        -------
        bool
            ``True`` if the attributes were successfully updated.
            ``False`` otherwise.

        Notes
        -----
        This method will produce a dialog for editing the attributes of the vertices.

        """
        return VertexModifier.update_vertex_attributes(self, vertices)

    def modify_faces(self, faces):
        """Modify the attributes of the faces of the mesh item.

        Parameters
        ----------
        faces : list
            The identifiers of the faces of which the attributes will be updated.

        Returns
        -------
        bool
            ``True`` if the attributes were successfully updated.
            ``False`` otherwise.

        Notes
        -----
        This method will produce a dialog for editing the attributes of the faces.

        """
        return FaceModifier.update_face_attributes(self, faces)

    def modify_edges(self, edges):
        """Modify the attributes of the edges of the mesh item.

        Parameters
        ----------
        edges : list
            The identifiers of the edges of which the attributes will be updated.

        Returns
        -------
        bool
            ``True`` if the attributes were successfully updated.
            ``False`` otherwise.

        Notes
        -----
        This method will produce a dialog for editing the attributes of the edges.

        """
        return EdgeModifier.update_edge_attributes(self, edges)

    def move(self):
        raise NotImplementedError

    def move_vertices(self, vertices):
        raise NotImplementedError


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pass
