from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino
from Rhino.Geometry import Point3d

import compas_rhino
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation
from compas.geometry import subtract_vectors
from compas.geometry import add_vectors
from compas.geometry import scale_vector
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

    """

    SETTINGS = {
        'color.vertices': (255, 255, 255),
        'color.edges': (0, 0, 0),
        'color.faces': (0, 0, 0),
        'color.mesh': (0, 0, 0),
        'show.mesh': True,
        'show.vertices': True,
        'show.edges': True,
        'show.faces': False,
        'show.vertexlabels': False,
        'show.facelabels': False,
        'show.edgelabels': False,
        'show.vertexnormals': False,
        'show.facenormals': False,
    }

    modify = mesh_update_attributes
    modify_vertices = mesh_update_vertex_attributes
    modify_faces = mesh_update_face_attributes
    modify_edges = mesh_update_edge_attributes

    def __init__(self, mesh, scene=None, name=None, layer=None, visible=True, settings=None):
        super(MeshObject, self).__init__(mesh, scene, name, layer, visible)
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
        self.settings.update(type(self).SETTINGS)
        if settings:
            self.settings.update(settings)

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

    # def __getstate__(self):
    #     pass

    # def __setstate__(self, state):
    #     pass

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

        if self.settings['show.vertices']:
            vertices = list(self.mesh.vertices())

            guids = self.artist.draw_vertices(vertices=vertices, color=self.settings['color.vertices'])
            self.guid_vertex = zip(guids, vertices)

            if self.settings['show.vertexlabels']:
                text = {vertex: str(vertex) for vertex in vertices}
                guids = self.artist.draw_vertexlabels(text=text, color=self.settings['color.vertices'])
                self.guid_vertexlabel = zip(guids, vertices)

            if self.settings['show.vertexnormals']:
                guids = self.artist.draw_vertexnormals(vertices=vertices, color=self.settings['color.vertices'])
                self.guid_vertexnormal = zip(guids, vertices)

        if self.settings['show.mesh']:
            guids = self.artist.draw_mesh(color=self.settings['color.mesh'], disjoint=True)
            self._guids = guids

        else:
            if self.settings['show.faces']:
                faces = list(self.mesh.faces())

                guids = self.artist.draw_faces(faces=faces, color=self.settings['color.faces'])
                self.guid_face = zip(guids, faces)

                if self.settings['show.facelabels']:
                    text = {face: str(face) for face in faces}
                    guids = self.artist.draw_facelabels(text=text, color=self.settings['color.faces'])
                    self.guid_facelabel = zip(guids, faces)

                if self.settings['show.facenormals']:
                    guids = self.artist.draw_facenormals(faces=faces, color=self.settings['color.faces'])
                    self.guid_face = zip(guids, faces)

        if self.settings['show.edges']:
            edges = list(self.mesh.edges())

            guids = self.artist.draw_edges(edges=edges, color=self.settings['color.edges'])
            self.guid_edge = zip(guids, edges)

            if self.settings['show.edgelabels']:
                text = {edge: "{}-{}".format(*edge) for edge in edges}
                guids = self.artist.draw_edgelabels(text=text, color=self.settings['color.edges'])
                self.guid_edgelabel = zip(guids, edges)

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

    def scale_from_3_points(self, message="Select the base vertex for the scaling operation."):
        """Scale the mesh object from 3 reference points.

        Note that this does not scale the underlying data structure,
        but only the scale of the representation in Rhino.

        The first reference point of the scaling operation must be a vertex of the mesh.
        This vertex will become the new anchor of the object.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.
        """
        def OnDynamicDraw(sender, e):
            d1 = p0.DistanceTo(p1)
            d2 = p0.DistanceTo(e.CurrentPoint)
            ratio = d2 / d1
            DrawLine = e.Display.DrawDottedLine
            for vertex in self.diagram.vertices():
                if vertex == anchor:
                    continue
                vector = vertex_vector[vertex]
                vertex_xyz[vertex] = add_vectors(origin, scale_vector(vector, ratio))
            for u, v in iter(edges):
                DrawLine(Point3d(* vertex_xyz[u]), Point3d(* vertex_xyz[v]), color)

        anchor = self.select_vertex(message=message)
        if anchor is None:
            return

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        edges = list(self.diagram.edges())
        vertex_xyz = self.artist.vertex_xyz
        vertex_xyz0 = {vertex: vertex_xyz[vertex][:] for vertex in vertex_xyz}

        origin = vertex_xyz0[anchor]
        vertex_vector = {vertex: subtract_vectors(vertex_xyz0[vertex], origin) for vertex in vertex_xyz}
        p0 = Point3d(* origin)

        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt('Select the 1st reference point.')
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False
        p1 = gp.Point()

        gp.SetCommandPrompt('Select the 2nd reference point.')
        gp.DynamicDraw += OnDynamicDraw
        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False
        p2 = gp.Point()

        d1 = p0.DistanceTo(p1)
        d2 = p0.DistanceTo(p2)
        ratio = d2 / d1
        self.scale *= ratio
        self.anchor = anchor
        self.location = vertex_xyz[anchor]
        return True


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pass
