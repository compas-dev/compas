from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation
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
        self._location = None
        self._scale = None
        self._rotation = None
        self._guid_vertex = {}
        self._guid_face = {}
        self._guid_edge = {}

    @property
    def mesh(self):
        return self.item

    @mesh.setter
    def mesh(self, mesh):
        self.item = mesh

    @property
    def location(self):
        """:class:`compas.geometry.Point`:
        The location of the object.
        Default is the origin of the world coordinate system.
        The object transformation is applied relative to this location.

        Setting this location will make a copy of the provided point object.
        Moving the original point will thus not affect the object's location.
        """
        if not self._location:
            self._location = Point(0, 0, 0)
        return self._location

    @location.setter
    def location(self, location):
        self._location = Point(*location)

    @property
    def scale(self):
        """float:
        A uniform scaling factor for the object in the scene.
        The scale is applied relative to the location of the object in the scene.
        """
        if not self._scale:
            self._scale = 1.0
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    @property
    def rotation(self):
        """list of float:
        The rotation angles around the 3 axis of the coordinate system
        with the origin placed at the location of the object in the scene.
        """
        if not self._rotation:
            self._rotation = [0, 0, 0]
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation

    @property
    def vertex_xyz(self):
        S = Scale.from_factors([self.scale] * 3)
        R = Rotation.from_euler_angles(self.rotation)
        T = Translation.from_vector(self.location)
        mesh = self.mesh.transformed(T * R * S)
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        return vertex_xyz

    def clear(self):
        self.artist.clear()

    def draw(self):
        """Draw the object representing the mesh.
        """
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz
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
