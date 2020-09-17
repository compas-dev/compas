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


__all__ = ['VolMeshObject']


class VolMeshObject(BaseObject):
    """Class for representing COMPAS volmeshes in Rhino.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A volmesh data structure.
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

    """

    SETTINGS = {
        'color.vertices': (255, 255, 255),
        'color.edges': (0, 0, 0),
        'color.faces': (210, 210, 210),
        'color.cells': (255, 0, 0),
        'show.vertices': True,
        'show.edges': True,
        'show.faces': True,
        'show.cells': False,
        'show.vertexlabels': False,
        'show.facelabels': False,
        'show.edgelabels': False,
        'show.celllabels': False,
    }

    modify = mesh_update_attributes
    modify_vertices = mesh_update_vertex_attributes
    modify_faces = mesh_update_face_attributes
    modify_edges = mesh_update_edge_attributes

    def __init__(self, volmesh, scene=None, name=None, layer=None, visible=True, settings=None):
        super(VolMeshObject, self).__init__(volmesh, scene, name, layer, visible)
        self._anchor = None
        self._location = None
        self._scale = None
        self._rotation = None
        self.settings.update(VolMeshObject.SETTINGS)
        if settings:
            self.settings.update(settings)

    @property
    def volmesh(self):
        return self.item

    @volmesh.setter
    def volmesh(self, volmesh):
        self.item = volmesh

    @property
    def anchor(self):
        """The vertex of the volmesh that is anchored to the location of the object."""
        return self._anchor

    @anchor.setter
    def anchor(self, vertex):
        if self.volmesh.has_vertex(vertex):
            self._anchor = vertex

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
        """dict : The view coordinates of the volmesh object."""
        origin = Point(0, 0, 0)
        if self.anchor is not None:
            xyz = self.volmesh.vertex_attributes(self.anchor, 'xyz')
            point = Point(* xyz)
            T1 = Translation.from_vector(origin - point)
            S = Scale.from_factors([self.scale] * 3)
            R = Rotation.from_euler_angles(self.rotation)
            T2 = Translation.from_vector(self.location)
            X = T2 * R * S * T1
        else:
            S = Scale.from_factors([self.scale] * 3)
            R = Rotation.from_euler_angles(self.rotation)
            T = Translation.from_vector(self.location)
            X = T * R * S
        volmesh = self.volmesh.transformed(X)
        vertex_xyz = {vertex: volmesh.vertex_attributes(vertex, 'xyz') for vertex in volmesh.vertices()}
        return vertex_xyz

    def clear(self):
        self.artist.clear()

    def draw(self):
        """Draw the volmesh using the visualisation settings.
        """
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz
        if self.settings['show.vertices']:
            self.artist.draw_vertices(color=self.settings['color.vertices'])
            if self.settings['show.vertexlabels']:
                self.artist.draw_vertexlabels(color=self.settings['color.vertices'])
        if self.settings['show.faces']:
            self.artist.draw_faces(color=self.settings['color.faces'])
            if self.settings['show.facelabels']:
                self.artist.draw_facelabels(color=self.settings['color.faces'])
        if self.settings['show.edges']:
            self.artist.draw_edges(color=self.settings['color.edges'])
            if self.settings['show.edgelabels']:
                self.artist.draw_edgelabels(color=self.settings['color.edges'])
        if self.settings['show.cells']:
            self.artist.draw_cells(color=self.settings['color.cells'])
            if self.settings['show.celllabels']:
                self.artist.draw_celllabels(color=self.settings['color.cells'])
        self.redraw()

    def select(self):
        # there is currently no "general" selection method
        # for the entire mesh object
        raise NotImplementedError

    def select_vertex(self, message="Select one vertex."):
        """Select one vertex of the mesh.

        Returns
        -------
        int
            A vertex identifier.
        """
        guid = compas_rhino.select_point(message=message)
        if guid and guid in self.guid_vertex:
            return self.guid_vertex[guid]

    def select_vertices(self, message="Select vertices."):
        """Select vertices of the volmesh.

        Returns
        -------
        list
            A list of vertex identifiers.
        """
        guids = compas_rhino.select_points(message=message)
        vertices = [self.artist.guid_vertex[guid] for guid in guids if guid in self.artist.guid_vertex]
        return vertices

    def select_faces(self, message="Select faces."):
        """Select faces of the volmesh.

        Returns
        -------
        list
            A list of face identifiers.
        """
        guids = compas_rhino.select_meshes(message=message)
        faces = [self.artist.guid_face[guid] for guid in guids if guid in self.artist.guid_face]
        return faces

    def select_edges(self, message="Select edges."):
        """Select edges of the volmesh.

        Returns
        -------
        list
            A list of edge identifiers.
        """
        guids = compas_rhino.select_lines(message=message)
        edges = [self.artist.guid_edge[guid] for guid in guids if guid in self.artist.guid_edge]
        return edges

    def move(self):
        """Move the entire volmesh object to a different location."""
        raise NotImplementedError

    def move_vertex(self, vertex):
        """Move a single vertex of the volmesh object and update the data structure accordingly.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.
        """
        return mesh_move_vertex(self.volmesh, vertex)

    def move_vertices(self, vertices):
        """Move a multiple vertices of the volmesh object and update the data structure accordingly.

        Parameters
        ----------
        vertices : list of int
            The identifiers of the vertices.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.
        """
        return mesh_move_vertices(self.volmesh, vertices)

    # it is not entirely clear what is meant with this in terms of face/halfface
    def move_face(self, face):
        """Move a single face of the volmesh object and update the data structure accordingly.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.
        """
        return mesh_move_face(self.volmesh, face)


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pass
