from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ast
import compas_rhino
from compas.geometry import add_vectors
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.utilities import is_color_rgb

import Rhino
from Rhino.Geometry import Point3d

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
    visible : bool, optional
        Toggle for the visibility of the object.
    layer : str, optional
        The layer for drawing.
    show_vertices : bool, optional
        Indicate that the verticess should be drawn when the mesh is visualised.
    show_edges : bool, optional
        Indicate that the edges should be drawn when the mesh is visualised.
    show_faces : bool, optional
        Indicate that the faces should be drawn when the mesh is visualised.
    vertextext : dict, optional
        A dictionary mapping vertex identifiers to text labels.
    edgetext : dict, optional
        A dictionary mapping edge identifiers to text labels.
    facetext : dict, optional
        A dictionary mapping face identifiers to text labels.
    vertexcolor : rgb color tuple or dict of rgb color tuples, optional
        A single RGB color value or a dictionary mapping vertex identifiers to RGB color values.
    edgecolor : rgb color tuple or dict of rgb color tuples, optional
        A single RGB color value or a dictionary mapping edge identifiers to RGB color values.
    facecolor : rgb color tuple or dict of rgb color tuples, optional
        A single RGB color value or a dictionary mapping face identifiers to RGB color values.
    """

    def __init__(self, mesh, scene=None, name=None, visible=True, layer=None,
                 show_vertices=False, show_edges=False, show_faces=True,
                 vertextext=None, edgetext=None, facetext=None,
                 vertexcolor=None, edgecolor=None, facecolor=None):
        super(MeshObject, self).__init__(mesh, scene, name, visible, layer)
        self._guids = []
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
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
    def guids(self):
        """list: The GUIDs of all Rhino objects created by this artist."""
        guids = self._guids
        guids += list(self.guid_vertex)
        guids += list(self.guid_edge)
        guids += list(self.guid_face)
        return guids

    @property
    def vertex_color(self):
        """dict: Dictionary mapping vertices to colors.

        Only RGB color values are allowed.
        If a single RGB color is assigned to this attribute instead of a dictionary of colors,
        a dictionary will be created automatically with the provided color mapped to all vertices.
        """
        if not self._vertex_color:
            self._vertex_color = {vertex: self.artist.default_vertexcolor for vertex in self.mesh.vertices()}
        return self._vertex_color

    @vertex_color.setter
    def vertex_color(self, vertex_color):
        if isinstance(vertex_color, dict):
            self._vertex_color = vertex_color
        elif is_color_rgb(vertex_color):
            self._vertex_color = {vertex: vertex_color for vertex in self.mesh.vertices()}

    @property
    def edge_color(self):
        """dict: Dictionary mapping edges to colors.

        Only RGB color values are allowed.
        If a single RGB color is assigned to this attribute instead of a dictionary of colors,
        a dictionary will be created automatically with the provided color mapped to all edges.
        """
        if not self._edge_color:
            self._edge_color = {edge: self.artist.default_edgecolor for edge in self.mesh.edges()}
        return self._edge_color

    @edge_color.setter
    def edge_color(self, edge_color):
        if isinstance(edge_color, dict):
            self._edge_color = edge_color
        elif is_color_rgb(edge_color):
            self._edge_color = {edge: edge_color for edge in self.mesh.edges()}

    @property
    def face_color(self):
        """dict: Dictionary mapping faces to colors.

        Only RGB color values are allowed.
        If a single RGB color is assigned to this attribute instead of a dictionary of colors,
        a dictionary will be created automatically with the provided color mapped to all faces.
        """
        if not self._face_color:
            self._face_color = {face: self.artist.default_facecolor for face in self.mesh.faces()}
        return self._face_color

    @face_color.setter
    def face_color(self, face_color):
        if isinstance(face_color, dict):
            self._face_color = face_color
        elif is_color_rgb(face_color):
            self._face_color = {face: face_color for face in self.mesh.faces()}

    def clear(self):
        """Clear all Rhino objects associated with this object.
        """
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}

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
            guids = self.artist.draw_faces(faces=faces, color=face_color)
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
        names = sorted(self.mesh.attributes.keys())
        values = [str(self.mesh.attributes[name]) for name in names]
        values = compas_rhino.update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                try:
                    self.mesh.attributes[name] = ast.literal_eval(value)
                except (ValueError, TypeError):
                    self.mesh.attributes[name] = value
            return True
        return False

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
        names = names or self.mesh.default_vertex_attributes.keys()
        names = sorted(names)
        values = self.mesh.vertex_attributes(vertices[0], names)
        if len(vertices) > 1:
            for i, name in enumerate(names):
                for vertex in vertices[1:]:
                    if values[i] != self.mesh.vertex_attribute(vertex, name):
                        values[i] = '-'
                        break
        values = map(str, values)
        values = compas_rhino.update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                if value == '-':
                    continue
                for vertex in vertices:
                    try:
                        self.mesh.vertex_attribute(vertex, name, ast.literal_eval(value))
                    except (ValueError, TypeError):
                        self.mesh.vertex_attribute(vertex, name, value)
            return True
        return False

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
        names = names or self.mesh.default_edge_attributes.keys()
        names = sorted(names)
        edge = edges[0]
        values = self.mesh.edge_attributes(edge, names)
        if len(edges) > 1:
            for i, name in enumerate(names):
                for edge in edges[1:]:
                    if values[i] != self.mesh.edge_attribute(edge, name):
                        values[i] = '-'
                        break
        values = map(str, values)
        values = compas_rhino.update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                if value == '-':
                    continue
                for edge in edges:
                    try:
                        value = ast.literal_eval(value)
                    except (SyntaxError, ValueError, TypeError):
                        pass
                    self.mesh.edge_attribute(edge, name, value)
            return True
        return False

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
        names = names or self.mesh.default_face_attributes.keys()
        names = sorted(names)
        values = self.mesh.face_attributes(faces[0], names)
        if len(faces) > 1:
            for i, name in enumerate(names):
                for face in faces[1:]:
                    if values[i] != self.mesh.face_attribute(face, name):
                        values[i] = '-'
                        break
        values = map(str, values)
        values = compas_rhino.update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                if value == '-':
                    continue
                for face in faces:
                    try:
                        self.mesh.face_attribute(face, name, ast.literal_eval(value))
                    except (ValueError, TypeError):
                        self.mesh.face_attribute(face, name, value)
            return True
        return False

    # not clear if this is now about the location or the data
    def move(self):
        """Move the entire mesh object to a different location."""
        raise NotImplementedError

    def move_vertex(self, vertex, constraint=None, allow_off=True):
        """Move a single vertex of the mesh object and update the data structure accordingly.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.
        constraint : :class:`Rhino.Geometry`, optional
            A Rhino geometry object to constrain the movement to.
            By default the movement is unconstrained.
        allow_off : bool, optional (True)
            Allow the vertex to move off the constraint.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.
        """
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs = [self.mesh.vertex_coordinates(nbr) for nbr in self.mesh.vertex_neighbors(vertex)]
        nbrs = [Point3d(*xyz) for xyz in nbrs]

        def OnDynamicDraw(sender, e):
            for ep in nbrs:
                sp = e.CurrentPoint
                e.Display.DrawDottedLine(sp, ep, color)

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt('Point to move to?')
        gp.DynamicDraw += OnDynamicDraw
        if constraint:
            gp.Constrain(constraint, allow_off)

        gp.Get()
        if gp.CommandResult() == Rhino.Commands.Result.Success:
            self.mesh.vertex_attributes(vertex, 'xyz', list(gp.Point()))
            return True
        return False

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
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for vertex in vertices:
            a = self.mesh.vertex_coordinates(vertex)
            nbrs = self.mesh.vertex_neighbors(vertex)
            for nbr in nbrs:
                b = self.mesh.vertex_coordinates(nbr)
                line = [Point3d(* a), Point3d(* b)]
                if nbr in vertices:
                    lines.append(line)
                else:
                    connectors.append(line)

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt('Point to move from?')
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        start = gp.Point()

        def OnDynamicDraw(sender, e):
            end = e.CurrentPoint
            vector = end - start
            for a, b in lines:
                a = a + vector
                b = b + vector
                e.Display.DrawDottedLine(a, b, color)
            for a, b in connectors:
                a = a + vector
                e.Display.DrawDottedLine(a, b, color)

        gp.SetCommandPrompt('Point to move to?')
        gp.SetBasePoint(start, False)
        gp.DrawLineFromPoint(start, True)
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        end = gp.Point()
        vector = list(end - start)

        for vertex in vertices:
            xyz = self.mesh.vertex_attributes(vertex, 'xyz')
            self.mesh.vertex_attributes(vertex, 'xyz', add_vectors(xyz, vector))
        return True

    def move_face(self, face, constraint=None, allow_off=True):
        """Move a single face of the mesh object and update the data structure accordingly.

        Parameters
        ----------
        face : int
            The identifier of the face.
        constraint : Rhino.Geometry (None)
            A Rhino geometry object to constrain the movement to.
            By default the movement is unconstrained.
        allow_off : bool (False)
            Allow the vertex to move off the constraint.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.
        """
        def OnDynamicDraw(sender, e):
            for ep in nbrs:
                sp = e.CurrentPoint
                e.Display.DrawDottedLine(sp, ep, color)

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs = [self.mesh.face_coordinates(nbr) for nbr in self.mesh.face_neighbors(face)]
        nbrs = [Point3d(*xyz) for xyz in nbrs]

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt('Point to move to?')
        gp.DynamicDraw += OnDynamicDraw
        if constraint:
            gp.Constrain(constraint, allow_off)

        gp.Get()

        if gp.CommandResult() == Rhino.Commands.Result.Success:
            self.mesh.face_attributes(face, 'xyz', list(gp.Point()))
            return True
        return False
