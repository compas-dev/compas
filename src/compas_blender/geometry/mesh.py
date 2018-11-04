
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    import bpy
except ImportError:
    pass

from compas.geometry import add_vectors
from compas.geometry import distance_point_point
from compas.geometry import subtract_vectors

from compas_blender.geometry import BlenderGeometry


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'BlenderMesh',
]


class BlenderMesh(BlenderGeometry):

    def __init__(self, object):
        super(BlenderMesh, self).__init__(obj=object)


    @classmethod
    def from_selection(cls):

        raise NotImplementedError


    @classmethod
    def from_name(cls, name):

        return BlenderMesh(object=bpy.data.objects[name])


    # ------------------------------------------------------------------------------------
    # Vertices
    # ------------------------------------------------------------------------------------

    def get_vertices_coordinates(self):

        return [add_vectors(self.location, i) for i in [list(i.co) for i in self.geometry.vertices]]


    def set_vertices_coordinates(self, xyzs):

        for index, xyz in xyzs.items():
            self.geometry.vertices[index].co = subtract_vectors(xyz, self.location)


    def get_vertices_colors(self, vertices=None):

        colors = {}
        col = self.geometry.vertex_colors.active

        if col:

            if not vertices:
                vertices = range(len(self.geometry.vertices))

            for face in self.geometry.polygons:
                for i in face.loop_indices:
                    j = self.geometry.loops[i].vertex_index

                    if (j in vertices) and (not colors.get(j, None)):
                        colors[j] = list(col.data[i].color)[:3]

            return colors

        return


    def set_vertices_colors(self, colors):

        if self.geometry.vertex_colors:
            col = self.geometry.vertex_colors.active
        else:
            col = self.geometry.vertex_colors.new()

        for face in self.geometry.polygons:
            for i in face.loop_indices:
                j = self.geometry.loops[i].vertex_index

                if j in colors:
                    col.data[i].color = list(colors[j]) + [1]


    def unset_vertices_colors(self):

        vertex_colors = self.geometry.vertex_colors

        while vertex_colors:
            vertex_colors.remove(vertex_colors[0])


    def get_vertex_index(self):

        raise NotImplementedError


    def get_vertices_indices(self):

        raise NotImplementedError


    def get_vertex_face_indices(self):

        raise NotImplementedError


    def get_vertices_face_indices(self):

        raise NotImplementedError


    # ------------------------------------------------------------------------------------
    # Edges
    # ------------------------------------------------------------------------------------

    def get_edges_vertex_indices(self, edges=None):

        if not edges:
            edges = range(len(self.geometry.edges))

        return {edge: list(self.geometry.edges[edge].vertices) for edge in edges}


    def get_edge_index(self):

        raise NotImplementedError


    def get_edges_indices(self):

        raise NotImplementedError


    def edge_length(self, edge):

        u, v = self.geometry.edges[edge].vertices
        sp, ep = [list(self.geometry.vertices[i].co) for i in [u, v]]

        return distance_point_point(sp, ep)


    def edges_lengths(self, edges):

        return [self.edge_length(edge=edge) for edge in edges]


    # ------------------------------------------------------------------------------------
    # Faces
    # ------------------------------------------------------------------------------------

    def get_faces_vertex_indices(self, faces=None):

        if not faces:
            faces = range(len(self.geometry.polygons))
        
        return [list(self.geometry.polygons[face].vertices) for face in faces]


    def get_faces_vertices(self, faces=None):

        if not faces:
            faces = range(len(self.geometry.polygons))

        return [[list(add_vectors(self.location, self.geometry.vertices[i].co)) for i in face]
                for face in self.get_faces_vertex_indices(faces=faces)]


    def get_face_index(self):

        raise NotImplementedError


    def get_faces_indices(self):

        raise NotImplementedError


    def face_normal(self, face):

        return list(self.geometry.polygons[face].normal)


    def faces_normals(self, faces=None):

        if not faces:
            faces = range(len(self.geometry.polygons))

        return [self.face_normal(face=face) for face in faces]


    def face_area(self, face):

        return self.geometry.polygons[face].area


    def faces_areas(self, faces=None):

        if not faces:
            faces = range(len(self.geometry.polygons))

        return [self.face_area(face=face) for face in faces]


    # ------------------------------------------------------------------------------------
    # Other
    # ------------------------------------------------------------------------------------

    def get_vertices_and_faces(self):

        vertices = self.get_vertices_coordinates()
        faces    = self.get_faces_vertex_indices()

        return vertices, faces


    def get_border(self):

        raise NotImplementedError


    def closest_point(self, point, maxdist=None):

        raise NotImplementedError


    def closest_points(self, points, maxdist=None):

        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    mesh = BlenderMesh.from_name('Cube')

    print(mesh.geometry)
    print(mesh.object)
    print(mesh.otype)
    print(mesh.name)
    print(mesh.location)

    print(mesh.get_vertices_coordinates())
    print(mesh.get_faces_vertex_indices())
    print(mesh.get_faces_vertices())
    print(mesh.get_vertices_and_faces())

    mesh.set_vertices_colors(colors={0: [1, 0, 0], 1: [0, 0, 1]})
    mesh.unset_vertices_colors()
    print(mesh.get_vertices_colors())

    mesh.set_vertices_coordinates({0: [0, 0, 0], 1: [1, 1, 0]})

    print(mesh.edges_lengths(edges=[2, 3]))
    print(mesh.get_edges_vertex_indices())

    print(mesh.faces_normals())
    print(mesh.faces_areas())

    mesh.refresh()
