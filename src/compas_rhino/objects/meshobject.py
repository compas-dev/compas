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
# from compas_rhino.objects.inspect import MeshVertexInspector


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

    modify = mesh_update_attributes
    modify_vertices = mesh_update_vertex_attributes
    modify_faces = mesh_update_face_attributes
    modify_edges = mesh_update_edge_attributes

    def __init__(self, mesh, scene=None, name=None, layer=None, visible=True, settings=None):
        super(MeshObject, self).__init__(mesh, scene, name, layer, visible)
        self._anchor = None
        self._location = None
        self._scale = None
        self._rotation = None
        self._inspector = None
        self.settings.update({
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
        })
        if settings:
            self.settings.update(settings)

    @property
    def mesh(self):
        return self.item

    @mesh.setter
    def mesh(self, mesh):
        self.item = mesh

    # @property
    # def inspector(self):
    #     """:class:`compas_rhino.objects.MeshVertexInspector`: An inspector conduit."""
    #     if not self._inspector:
    #         self._inspector = MeshVertexInspector(self.diagram)
    #     return self._inspector

    @property
    def anchor(self):
        """"""
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

    def clear(self):
        self.artist.clear()

    def draw(self):
        """Draw the object representing the mesh.
        """
        self.clear()
        if not self.visible:
            return
        self.artist.vertex_xyz = self.vertex_xyz
        if self.settings['show.vertices']:
            self.artist.draw_vertices(color=self.settings['color.vertices'])
            if self.settings['show.vertexlabels']:
                self.artist.draw_vertexlabels(color=self.settings['color.vertices'])
            if self.settings['show.vertexnormals']:
                self.artist.draw_vertexnormals(color=self.settings['color.vertices'])
        if self.settings['show.mesh']:
            self.artist.draw_mesh(color=self.settings['color.mesh'], disjoint=True)
        else:
            if self.settings['show.faces']:
                self.artist.draw_faces(color=self.settings['color.faces'])
                if self.settings['show.facelabels']:
                    self.artist.draw_facelabels(color=self.settings['color.faces'])
                if self.settings['show.facenormals']:
                    self.artist.draw_facenormals(color=self.settings['color.faces'])
        if self.settings['show.edges']:
            self.artist.draw_edges(color=self.settings['color.edges'])
            if self.settings['show.edgelabels']:
                self.artist.draw_edgelabels(color=self.settings['color.edges'])
        self.redraw()

    def select(self):
        raise NotImplementedError

    def select_vertices(self, message="Select vertices."):
        """Select vertices of the mesh.

        Returns
        -------
        list
            A list of vertex identifiers.
        """
        guids = compas_rhino.select_points(message=message)
        vertices = [self.artist.guid_vertex[guid] for guid in guids if guid in self.artist.guid_vertex]
        return vertices

    def select_faces(self, message="Select faces."):
        """Select faces of the mesh.

        Returns
        -------
        list
            A list of face identifiers.
        """
        guids = compas_rhino.select_meshes(message=message)
        faces = [self.artist.guid_face[guid] for guid in guids if guid in self.artist.guid_face]
        return faces

    def select_edges(self, message="Select edges."):
        """Select edges of the mesh.

        Returns
        -------
        list
            A list of edge identifiers.
        """
        guids = compas_rhino.select_lines(message=message)
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

    # def inspector_on(self):
    #     """Turn on the diagram inspector conduit."""
    #     self.inspector.vertex_xyz = self.artist.vertex_xyz
    #     self.inspector.enable()

    # def inspector_off(self):
    #     """Turn off the diagram inspector conduit."""
    #     self.inspector.disable()

    def scale_from_2_points(self):
        """Scale the mesh object from 2 reference points.

        Note that this does not scale the underlying data structure,
        but only the scale of the representation in Rhino.

        The origin of the scaling operation is the anchor of the object.

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
                xyz = self.diagram.vertex_attributes(vertex, 'xyz')
                vector = subtract_vectors(xyz, anchor_xyz)
                vertex_xyz[vertex] = add_vectors(origin, scale_vector(vector, self.artist.scale * ratio))
            for u, v in iter(edges):
                DrawLine(Point3d(* vertex_xyz[u]), Point3d(* vertex_xyz[v]), color)

        if self.anchor is None:
            return False

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        vertex_xyz = self.artist.vertex_xyz
        edges = list(self.diagram.edges())
        anchor_xyz = self.diagram.vertex_attributes(self.anchor, 'xyz')
        origin = list(self.location)
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
        return True


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pass
