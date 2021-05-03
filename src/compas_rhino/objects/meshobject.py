from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation

from compas_rhino.objects._modify import mesh_update_attributes
from compas_rhino.objects._modify import mesh_update_vertex_attributes
from compas_rhino.objects._modify import mesh_update_face_attributes
from compas_rhino.objects._modify import mesh_update_edge_attributes
from compas_rhino.objects._modify import mesh_move_vertex
from compas_rhino.objects._modify import mesh_move_vertices
from compas_rhino.objects._modify import mesh_move_face

from ._object import Object


__all__ = ['MeshObject']


class MeshObject(Object):
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

    """

    default_vertexcolor = (255, 255, 255)
    default_edgecolor = (0, 0, 0)
    default_facecolor = (0, 0, 0)

    def __init__(self, mesh, scene=None, name=None, visible=True, layer=None,
                 show_faces=True, show_vertices=False, show_edges=False,
                 vertextext=None, edgetext=None, facetext=None,
                 vertexcolor=None, edgecolor=None, facecolor=None):
        super(MeshObject, self).__init__(mesh, scene, name, visible, layer)
        self._guids = []
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_vertexnormal = {}
        self._guid_facenormal = {}
        self._guid_vertexlabel = {}
        self._guid_edgelabel = {}
        self._guid_facelabel = {}
        self._anchor = None
        self._location = None
        self._scale = None
        self._rotation = None
        self._vertex_color = None
        self._edge_color = None
        self._face_color = None
        self._vertex_text = None
        self._edge_text = None
        self._face_text = None
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        self.vertex_color = vertexcolor
        self.edge_color = edgecolor
        self.face_color = facecolor
        self.vertex_text = vertextext
        self.edge_text = edgetext
        self.face_text = facetext

    @property
    def mesh(self):
        return self.item

    @mesh.setter
    def mesh(self, mesh):
        self.item = mesh
        self._guids = []
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_vertexnormal = {}
        self._guid_facenormal = {}
        self._guid_vertexlabel = {}
        self._guid_edgelabel = {}
        self._guid_facelabel = {}

    @property
    def anchor(self):
        """The vertex of the mesh that is anchored to the location of the object."""
        return self._anchor

    @anchor.setter
    def anchor(self, vertex):
        if self.mesh.has_vertex(vertex):
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
        """dict : The view coordinates of the mesh object."""
        origin = Point(0, 0, 0)
        if self.anchor is not None:
            xyz = self.mesh.vertex_attributes(self.anchor, 'xyz')
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
        mesh = self.mesh.transformed(X)
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        return vertex_xyz

    @property
    def guid_vertex(self):
        """dict: Map between Rhino object GUIDs and mesh vertex identifiers."""
        return self._guid_vertex

    @guid_vertex.setter
    def guid_vertex(self, values):
        self._guid_vertex = dict(values)

    @property
    def guid_edge(self):
        """dict: Map between Rhino object GUIDs and mesh edge identifiers."""
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    @property
    def guid_face(self):
        """dict: Map between Rhino object GUIDs and mesh face identifiers."""
        return self._guid_face

    @guid_face.setter
    def guid_face(self, values):
        self._guid_face = dict(values)

    @property
    def guid_vertexnormal(self):
        """dict: Map between Rhino object GUIDs and mesh vertexnormal identifiers."""
        return self._guid_vertexnormal

    @guid_vertexnormal.setter
    def guid_vertexnormal(self, values):
        self._guid_vertexnormal = dict(values)

    @property
    def guid_facenormal(self):
        """dict: Map between Rhino object GUIDs and mesh facenormal identifiers."""
        return self._guid_facenormal

    @guid_facenormal.setter
    def guid_facenormal(self, values):
        self._guid_facenormal = dict(values)

    @property
    def guid_vertexlabel(self):
        """dict: Map between Rhino object GUIDs and mesh vertexlabel identifiers."""
        return self._guid_vertexlabel

    @guid_vertexlabel.setter
    def guid_vertexlabel(self, values):
        self._guid_vertexlabel = dict(values)

    @property
    def guid_facelabel(self):
        """dict: Map between Rhino object GUIDs and mesh facelabel identifiers."""
        return self._guid_facelabel

    @guid_facelabel.setter
    def guid_facelabel(self, values):
        self._guid_facelabel = dict(values)

    @property
    def guid_edgelabel(self):
        """dict: Map between Rhino object GUIDs and mesh edgelabel identifiers."""
        return self._guid_edgelabel

    @guid_edgelabel.setter
    def guid_edgelabel(self, values):
        self._guid_edgelabel = dict(values)

    @property
    def guids(self):
        """list: The GUIDs of all Rhino objects created by this artist."""
        guids = self._guids
        guids += list(self.guid_vertex.keys())
        guids += list(self.guid_edge.keys())
        guids += list(self.guid_face.keys())
        guids += list(self.guid_vertexnormal.keys())
        guids += list(self.guid_facenormal.keys())
        guids += list(self.guid_vertexlabel.keys())
        guids += list(self.guid_edgelabel.keys())
        guids += list(self.guid_facelabel.keys())
        return guids

    @property
    def vertex_color(self):
        """dict: Dictionary mapping vertices to colors."""
        if not self._vertex_color:
            self._vertex_color = {vertex: self.default_vertexcolor for vertex in self.mesh.vertices()}
        return self._vertex_color

    @vertex_color.setter
    def vertex_color(self, vertex_color):
        if isinstance(vertex_color, dict):
            self._vertex_color = vertex_color
        elif len(vertex_color) == 3:
            if all(isinstance(c, (int, float)) for c in vertex_color):
                self._vertex_color = {vertex: vertex_color for vertex in self.mesh.vertices()}

    @property
    def edge_color(self):
        """dict: Dictionary mapping edges to colors."""
        if not self._edge_color:
            self._edge_color = {edge: self.default_edgecolor for edge in self.mesh.edges()}
        return self._edge_color

    @edge_color.setter
    def edge_color(self, edge_color):
        if isinstance(edge_color, dict):
            self._edge_color = edge_color
        elif len(edge_color) == 3:
            if all(isinstance(c, (int, float)) for c in edge_color):
                self._edge_color = {edge: edge_color for edge in self.mesh.edges()}

    @property
    def face_color(self):
        """dict: Dictionary mapping faces to colors."""
        if not self._face_color:
            self._face_color = {face: self.default_facecolor for face in self.mesh.faces()}
        return self._face_color

    @face_color.setter
    def face_color(self, face_color):
        if isinstance(face_color, dict):
            self._face_color = face_color
        elif len(face_color) == 3:
            if all(isinstance(c, (int, float)) for c in face_color):
                self._face_color = {face: face_color for face in self.mesh.faces()}

    def clear(self):
        """Clear all Rhino objects associated with this object.
        """
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_vertexnormal = {}
        self._guid_facenormal = {}
        self._guid_vertexlabel = {}
        self._guid_edgelabel = {}
        self._guid_facelabel = {}

    def draw(self):
        """Draw the object representing the mesh.
        """
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz

        if self.show_vertices:
            vertices = list(self.mesh.vertices())
            vertex_color = self.vertex_color
            guids = self.artist.draw_vertices(vertices=vertices, color=vertex_color)
            self.guid_vertex = zip(guids, vertices)

        if self.show_faces:
            faces = list(self.mesh.faces())
            face_color = self.face_color
            guids = self.artist.draw_faces(faces=faces, join_faces=True, color=face_color)
            self.guid_face = zip(guids, faces)

        if self.show_edges:
            edges = list(self.mesh.edges())
            edge_color = self.edge_color
            guids = self.artist.draw_edges(edges=edges, color=edge_color)
            self.guid_edge = zip(guids, edges)

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
        """Select vertices of the mesh.

        Returns
        -------
        list
            A list of vertex identifiers.
        """
        guids = compas_rhino.select_points(message=message)
        vertices = [self.guid_vertex[guid] for guid in guids if guid in self.guid_vertex]
        return vertices

    def select_faces(self, message="Select faces."):
        """Select faces of the mesh.

        Returns
        -------
        list
            A list of face identifiers.
        """
        guids = compas_rhino.select_meshes(message=message)
        faces = [self.guid_face[guid] for guid in guids if guid in self.guid_face]
        return faces

    def select_edges(self, message="Select edges."):
        """Select edges of the mesh.

        Returns
        -------
        list
            A list of edge identifiers.
        """
        guids = compas_rhino.select_lines(message=message)
        edges = [self.guid_edge[guid] for guid in guids if guid in self.guid_edge]
        return edges

    def modify(self):
        """Update the attributes of the mesh.

        Returns
        -------
        bool
            ``True`` if the update was successful.
            ``False`` otherwise.
        """
        return mesh_update_attributes(self.mesh)

    def modify_vertices(self, vertices, names=None):
        """Update the attributes of selected vertices.

        Parameters
        ----------
        vertices : list
            The vertices of the vertices of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is to update all available attributes.

        Returns
        -------
        bool
            True if the attributes were successfully updated.
            False otherwise.

        """
        return mesh_update_vertex_attributes(self.mesh, vertices, names=names)

    def modify_edges(self, edges, names=None):
        """Update the attributes of the edges.

        Parameters
        ----------
        edges : list
            The edges to update.
        names : list, optional
            The names of the atrtibutes to update.
            Default is to update all attributes.

        Returns
        -------
        bool
            ``True`` if the update was successful.
            ``False`` otherwise.

        """
        return mesh_update_edge_attributes(self.mesh, edges, names=names)

    def modify_faces(self, faces, names=None):
        """Update the attributes of selected faces.

        Parameters
        ----------
        vertices : list
            The vertices of the vertices of which the attributes should be updated.
        names : list, optional
            The names of the attributes that should be updated.
            Default is to update all available attributes.

        Returns
        -------
        bool
            True if the attributes were successfully updated.
            False otherwise.

        """
        return mesh_update_face_attributes(self.mesh, faces, names=names)

    # not clear if this is now about the location or the data
    def move(self):
        """Move the entire mesh object to a different location."""
        raise NotImplementedError

    def move_vertex(self, vertex):
        """Move a single vertex of the mesh object and update the data structure accordingly.

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
        return mesh_move_vertex(self.mesh, vertex)

    def move_vertices(self, vertices):
        """Move a multiple vertices of the mesh object and update the data structure accordingly.

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
        return mesh_move_vertices(self.mesh, vertices)

    def move_face(self, face):
        """Move a single face of the mesh object and update the data structure accordingly.

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
        return mesh_move_face(self.mesh, face)
