import bpy
import bmesh

from compas.datastructures import Mesh
from compas.geometry import Point

from ._geometry import BlenderGeometry


class BlenderMesh(BlenderGeometry):
    """Wrapper for Blender meshes.

    Attributes
    ----------
    object : :blender:`bpy.types.Object`
        The Blender scene object.
    geometry : :blender:`bpy.types.Mesh`
        The mesh data block.
    bmesh : :blender:`bpy.types.BMesh`
        The mesh data structure.
    location : :class:`~compas.geometry.Point`
        The location of the object in the scene.
    vertices : List[:class:`~compas.geometry.Point`]
        The mesh vertex locations.
    faces : List[List[:obj:`int`]]
        The mesh face vertices.

    Examples
    --------
    .. code-block:: python

        import os
        import compas
        from compas_blender.conversions import BlenderMesh

        mesh = BlenderMesh.from_monkey().to_compas()
        mesh = mesh.subdivide(k=2)

        path = os.path.join(os.path.expanduser(~), 'Desktop', 'monkey.json')

        compas.json_dump(mesh, path)

    """

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, obj):
        mesh = bpy.data.meshes.new_from_object(obj)
        self._object = obj
        self._geometry = mesh

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, data):
        self._object = None
        self._geometry = data

    @property
    def bmesh(self):
        return bmesh.from_edit_mesh(self.mesh)

    @property
    def location(self):
        if self.object:
            return Point(self.object.location)
        return Point(0, 0, 0)

    @property
    def vertices(self):
        point = self.location
        return [point + list(vertex.co) for vertex in self.geometry.vertices]

    @property
    def faces(self):
        return [list(face.vertices) for face in self.geometry.polygons]

    @classmethod
    def from_bmesh(cls, bm, name=None, free=True):
        """Construct a Blender mesh wrappper from a BMesh.

        Parameters
        ----------
        bm : :blender:`bpy.types.BMesh`
            The Blender mesh data structure.
        name : :obj:`str`, optional
            The name of the data block.
        free : :obj:`bool`, optional
            Free the data structure once the data block is created.

        Returns
        -------
        :class:`~compas_blender.conversions.BlenderMesh`

        """
        data = bpy.data.meshes.new(name or "Mesh")
        bm.to_mesh(data)
        if free:
            bm.free()
        mesh = cls()
        mesh.geometry = data
        return mesh

    @classmethod
    def from_monkey(cls, name=None):
        """Construct a Blender mesh wrappper from the Blender monkey.

        Parameters
        ----------
        name : :obj:`str`, optional
            The name of the data block.

        Returns
        -------
        :class:`~compas_blender.conversions.BlenderMesh`

        """
        bm = bmesh.new()
        bmesh.ops.create_monkey(bm)
        data = bpy.data.meshes.new(name or "Mesh")
        bm.to_mesh(data)
        bm.free()
        mesh = cls()
        mesh.geometry = data
        return mesh

    def to_compas(self, cls=None):
        """Convert the Blender mesh to a COMPAS mesh.

        Parameters
        ----------
        cls : :class:`~compas.datastructures.Mesh`, optional
            The type of COMPAS mesh.

        Returns
        -------
        :class:`~compas.datastructure.Mesh`

        """
        cls = cls or Mesh
        return cls.from_vertices_and_faces(self.vertices, self.faces)

    # def get_vertex_coordinates(self, vertex):
    #     return add_vectors(self.location, self.geometry.vertices[vertex].co)

    # def get_vertices_coordinates(self):
    #     xyzs = [vertex.co for vertex in self.geometry.vertices]
    #     return {vertex: add_vectors(self.location, xyz) for vertex, xyz in enumerate(xyzs)}

    # def set_vertices_coordinates(self, xyzs):
    #     for vertex, xyz in xyzs.items():
    #         self.geometry.vertices[vertex].co = subtract_vectors(xyz, self.location)

    # def get_vertices_colors(self, vertices=None):
    #     colors = {}
    #     col = self.geometry.vertex_colors.active
    #     if col:
    #         if not vertices:
    #             vertices = range(len(self.geometry.vertices))
    #         for face in self.geometry.polygons:
    #             for i in face.loop_indices:
    #                 j = self.geometry.loops[i].vertex_index
    #                 if (j in vertices) and (not colors.get(j, None)):
    #                     colors[j] = list(col.data[i].color)[:3]
    #         return colors

    # def set_vertices_colors(self, colors):
    #     if self.geometry.vertex_colors:
    #         col = self.geometry.vertex_colors.active
    #     else:
    #         col = self.geometry.vertex_colors.new()
    #     for face in self.geometry.polygons:
    #         for i in face.loop_indices:
    #             j = self.geometry.loops[i].vertex_index
    #             if j in colors:
    #                 col.data[i].color = list(colors[j]) + [1]

    # def unset_vertices_colors(self):
    #     vertex_colors = self.geometry.vertex_colors
    #     while vertex_colors:
    #         vertex_colors.remove(vertex_colors[0])

    # def get_edge_vertex_indices(self, edge):
    #     return list(self.geometry.edges[edge].vertices)

    # def get_edges_vertex_indices(self, edges=None):
    #     if not edges:
    #         edges = range(len(self.geometry.edges))
    #     return {edge: self.get_edge_vertex_indices(edge=edge) for edge in edges}

    # def edge_length(self, edge):
    #     u, v = self.geometry.edges[edge].vertices
    #     sp, ep = [list(self.geometry.vertices[i].co) for i in [u, v]]
    #     return distance_point_point(sp, ep)

    # def edges_lengths(self, edges=None):
    #     if not edges:
    #         edges = range(len(self.geometry.edges))
    #     return {edge: self.edge_length(edge=edge) for edge in edges}

    # def get_face_vertex_indices(self, face):
    #     return list(self.geometry.polygons[face].vertices)

    # def get_faces_vertex_indices(self, faces=None):
    #     if not faces:
    #         faces = range(len(self.geometry.polygons))
    #     return {face: self.get_face_vertex_indices(face=face) for face in faces}

    # def face_normal(self, face):
    #     return list(self.geometry.polygons[face].normal)

    # def faces_normals(self, faces=None):
    #     if not faces:
    #         faces = range(len(self.geometry.polygons))
    #     return {face: self.face_normal(face=face) for face in faces}

    # def face_area(self, face):
    #     return self.geometry.polygons[face].area

    # def faces_areas(self, faces=None):
    #     if not faces:
    #         faces = range(len(self.geometry.polygons))
    #     return {face: self.face_area(face=face) for face in faces}

    # def bevel(self, width=0.2, segments=1, only_vertices=False):
    #     self.object.modifiers.new('bevel', type='BEVEL')
    #     self.object.modifiers['bevel'].width = width
    #     self.object.modifiers['bevel'].segments = segments
    #     self.object.modifiers['bevel'].use_only_vertices = only_vertices
    #     self.refresh()

    # def subdivide(self, levels=1, type='SIMPLE'):
    #     self.object.modifiers.new('subdivision', type='SUBSURF')
    #     self.object.modifiers['subdivision'].levels = levels
    #     self.object.modifiers['subdivision'].subdivision_type = type  # or 'CATMULL_CLARK'
    #     self.refresh()

    # def triangulate(self):
    #     self.object.modifiers.new('triangulate', type='TRIANGULATE')
    #     self.refresh()

    # def get_vertices_and_faces(self):
    #     vertices = self.get_vertices_coordinates()
    #     faces = self.get_faces_vertex_indices()
    #     return vertices, faces
