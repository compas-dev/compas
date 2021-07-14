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

import Rhino
from Rhino.Geometry import Point3d

from ._object import Object


__all__ = ['VolMeshObject']


class VolMeshObject(Object):
    """Class for representing COMPAS volmeshes in Rhino.

    Parameters
    ----------
    volmesh : :class:`compas.datastructures.VolMesh`
        A volmesh data structure.
    scene : :class:`compas.scenes.Scene`, optional
        A scene object.
    name : str, optional
        The name of the object.
    visible : bool, optional
        Toggle for the visibility of the object.
    layer : str, optional
        The layer for drawing.
    show_vertices : bool, optional
        Indicate that the verticess should be drawn when the volmesh is visualised.
    show_edges : bool, optional
        Indicate that the edges should be drawn when the volmesh is visualised.
    show_faces : bool, optional
        Indicate that the faces should be drawn when the volmesh is visualised.
    show_cells : bool, optional
        Indicate that the cells should be drawn when the volmesh is visualised.
    vertextext : dict, optional
        A dictionary mapping vertex identifiers to text labels.
    edgetext : dict, optional
        A dictionary mapping edge identifiers to text labels.
    facetext : dict, optional
        A dictionary mapping face identifiers to text labels.
    celltext : dict, optional
        A dictionary mapping cell identifiers to text labels.
    vertexcolor : rgb color tuple or dict of rgb color tuples, optional
        A single RGB color value or a dictionary mapping vertex identifiers to RGB color values.
    edgecolor : rgb color tuple or dict of rgb color tuples, optional
        A single RGB color value or a dictionary mapping edge identifiers to RGB color values.
    facecolor : rgb color tuple or dict of rgb color tuples, optional
        A single RGB color value or a dictionary mapping face identifiers to RGB color values.
    cellcolor : rgb color tuple or dict of rgb color tuples, optional
        A single RGB color value or a dictionary mapping cell identifiers to RGB color values.

    """

    def __init__(self, volmesh, scene=None, name=None, visible=True, layer=None,
                 show_vertices=False, show_edges=False, show_faces=True, show_cells=True,
                 vertextext=None, edgetext=None, facetext=None, celltext=None,
                 vertexcolor=None, edgecolor=None, facecolor=None, cellcolor=None):
        super(VolMeshObject, self).__init__(volmesh, scene, name, visible, layer)
        self._guids = []
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_cell = {}
        self._anchor = None
        self._location = None
        self._scale = None
        self._rotation = None
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        self.show_cells = show_cells
        self.artist.vertex_color = vertexcolor
        self.artist.edge_color = edgecolor
        self.artist.face_color = facecolor
        self.artist.cell_color = cellcolor
        self.artist.vertex_text = vertextext
        self.artist.edge_text = edgetext
        self.artist.face_text = facetext
        self.artist.cell_text = celltext

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

    @property
    def guid_vertex(self):
        """Map between Rhino object GUIDs and volmesh vertex identifiers."""
        return self._guid_vertex

    @guid_vertex.setter
    def guid_vertex(self, values):
        self._guid_vertex = dict(values)

    @property
    def guid_edge(self):
        """Map between Rhino object GUIDs and volmsh edge identifiers."""
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    @property
    def guid_face(self):
        """Map between Rhino object GUIDs and volmesh face identifiers."""
        return self._guid_face

    @guid_face.setter
    def guid_face(self, values):
        self._guid_face = dict(values)

    @property
    def guid_cell(self):
        """Map between Rhino object GUIDs and volmesh face identifiers."""
        return self._guid_cell

    @guid_cell.setter
    def guid_cell(self, values):
        self._guid_cell = dict(values)

    @property
    def guids(self):
        """list: The GUIDs of all Rhino objects created by this artist."""
        guids = self._guids
        guids += list(self.guid_vertex)
        guids += list(self.guid_edge)
        guids += list(self.guid_face)
        guids += list(self.guid_cell)
        return guids

    def clear(self):
        """Clear all objects previously drawn by this artist.
        """
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guid_vertex = {}
        self._guid_edge = {}
        self._guid_face = {}
        self._guid_cell = {}

    def draw(self):
        """Draw the volmesh using the visualisation settings.
        """
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz

        if self.show_vertices:
            guids = self.artist.draw_vertices()
            self.guid_vertex = zip(guids, self.volmesh.vertices())

        if self.show_edges:
            guids = self.artist.draw_edges()
            self.guid_edge = zip(guids, self.volmesh.edges())

        if self.show_faces:
            guids = self.artist.draw_faces()
            self.guid_face = zip(guids, self.volmesh.faces())

        if self.show_cells:
            guids = self.artist.draw_cells()
            self.guid_cell = zip(guids, self.volmesh.cells())

    def select(self):
        # there is currently no "general" selection method
        # for the entire mesh object
        raise NotImplementedError

    def select_vertex(self, message="Select one vertex."):
        """Select one vertex of the volmesh.

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
        vertices = [self.guid_vertex[guid] for guid in guids if guid in self.guid_vertex]
        return vertices

    def select_faces(self, message="Select faces."):
        """Select faces of the volmesh.

        Returns
        -------
        list
            A list of face identifiers.
        """
        guids = compas_rhino.select_meshes(message=message)
        faces = [self.guid_face[guid] for guid in guids if guid in self.guid_face]
        return faces

    def select_edges(self, message="Select edges."):
        """Select edges of the volmesh.

        Returns
        -------
        list
            A list of edge identifiers.
        """
        guids = compas_rhino.select_lines(message=message)
        edges = [self.guid_edge[guid] for guid in guids if guid in self.guid_edge]
        return edges

    def modify(self):
        """Update the attributes of the volmesh.

        Returns
        -------
        bool
            ``True`` if the update was successful.
            ``False`` otherwise.
        """
        names = sorted(self.volmesh.attributes.keys())
        values = [str(self.volmesh.attributes[name]) for name in names]
        values = compas_rhino.update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                try:
                    self.volmesh.attributes[name] = ast.literal_eval(value)
                except (ValueError, TypeError):
                    self.volmesh.attributes[name] = value
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
        names = names or self.volmesh.default_vertex_attributes.keys()
        names = sorted(names)
        values = self.volmesh.vertex_attributes(vertices[0], names)
        if len(vertices) > 1:
            for i, name in enumerate(names):
                for vertex in vertices[1:]:
                    if values[i] != self.volmesh.vertex_attribute(vertex, name):
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
                        self.volmesh.vertex_attribute(vertex, name, ast.literal_eval(value))
                    except (ValueError, TypeError):
                        self.volmesh.vertex_attribute(vertex, name, value)
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
        names = names or self.volmesh.default_edge_attributes.keys()
        names = sorted(names)
        edge = edges[0]
        values = self.volmesh.edge_attributes(edge, names)
        if len(edges) > 1:
            for i, name in enumerate(names):
                for edge in edges[1:]:
                    if values[i] != self.volmesh.edge_attribute(edge, name):
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
                    self.volmesh.edge_attribute(edge, name, value)
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
        names = names or self.volmesh.default_face_attributes.keys()
        names = sorted(names)
        values = self.volmesh.face_attributes(faces[0], names)
        if len(faces) > 1:
            for i, name in enumerate(names):
                for face in faces[1:]:
                    if values[i] != self.volmesh.face_attribute(face, name):
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
                        self.volmesh.face_attribute(face, name, ast.literal_eval(value))
                    except (ValueError, TypeError):
                        self.volmesh.face_attribute(face, name, value)
            return True
        return False

    def move(self):
        """Move the entire volmesh object to a different location."""
        raise NotImplementedError

    def move_vertex(self, vertex, constraint=None, allow_off=True):
        """Move a single vertex of the volmesh object and update the data structure accordingly.

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
        nbrs = [self.volmesh.vertex_coordinates(nbr) for nbr in self.volmesh.vertex_neighbors(vertex)]
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
            self.volmesh.vertex_attributes(vertex, 'xyz', list(gp.Point()))
            return True
        return True

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
        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        lines = []
        connectors = []

        for vertex in vertices:
            a = self.volmesh.vertex_coordinates(vertex)
            nbrs = self.volmesh.vertex_neighbors(vertex)
            for nbr in nbrs:
                b = self.volmesh.vertex_coordinates(nbr)
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
            xyz = self.volmesh.vertex_attributes(vertex, 'xyz')
            self.volmesh.vertex_attributes(vertex, 'xyz', add_vectors(xyz, vector))
        return True

    # it is not entirely clear what is meant with this in terms of face/halfface
    def move_face(self, face, constraint=None, allow_off=True):
        """Move a single face of the volmesh object and update the data structure accordingly.

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
        nbrs = [self.volmesh.face_coordinates(nbr) for nbr in self.volmesh.face_neighbors(face)]
        nbrs = [Point3d(*xyz) for xyz in nbrs]

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt('Point to move to?')
        gp.DynamicDraw += OnDynamicDraw
        if constraint:
            gp.Constrain(constraint, allow_off)

        gp.Get()

        if gp.CommandResult() == Rhino.Commands.Result.Success:
            self.volmesh.face_attributes(face, 'xyz', list(gp.Point()))
            return True
        return False
