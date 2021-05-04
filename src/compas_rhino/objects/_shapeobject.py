from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.geometry import Point
from compas.geometry import Scale, Translation, Rotation
from compas_rhino.objects._object import Object


class ShapeObject(Object):

    def __init__(self, shape, scene=None, name=None, visible=True, layer=None,
                 show_faces=True, show_vertices=False, show_edges=False, join_faces=True, color=None):
        super(ShapeObject, self).__init__(shape, scene, name, visible, layer)
        self._mesh = None
        self._guids = []
        self._location = None
        self._scale = None
        self._rotation = None
        self._color = None
        self.show_vertices = show_vertices
        self.show_edges = show_edges
        self.show_faces = show_faces
        self.join_faces = join_faces
        self.color = color

    @property
    def shape(self):
        return self.item

    @shape.setter
    def shape(self, shape):
        self.item = shape
        self._mesh = None
        self._location = None
        self._scale = None
        self._rotation = None
        self._guids = []

    @property
    def mesh(self):
        raise NotImplementedError

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
            self._location = self.shape.frame.point
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
        T1 = Translation.from_vector(Point(0, 0, 0) - self.shape.frame.point)
        S = Scale.from_factors([self.scale] * 3)
        R = Rotation.from_euler_angles(self.rotation)
        T2 = Translation.from_vector(self.location)
        X = T2 * R * S * T1
        mesh = self.mesh.transformed(X)
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, 'xyz') for vertex in mesh.vertices()}
        return vertex_xyz

    @property
    def guids(self):
        """list: The GUIDs of all Rhino objects created by this artist."""
        return self._guids

    def draw(self):
        guids = []
        vertex_xyz = self.vertex_xyz
        if self.show_vertices:
            points = [{'pos': vertex_xyz[vertex], 'color': self.color} for vertex in self.mesh.vertices()]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        if self.show_edges:
            lines = [{'start': vertex_xyz[u], 'end': vertex_xyz[v], 'color': self.color} for u, v in self.mesh.edges()]
            guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        if self.show_faces:
            polygons = [{'points': [vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]} for face in self.mesh.faces()]
            temp = compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
            if self.join_faces:
                guid = compas_rhino.rs.JoinMeshes(temp, delete_input=True)
                compas_rhino.rs.ObjectLayer(guid, self.layer)
                compas_rhino.rs.ObjectName(guid, '{}'.format(self.name))
                compas_rhino.rs.ObjectColor(guid, self.color)
                temp = [guid]
            guids += temp
        self._guids = guids
