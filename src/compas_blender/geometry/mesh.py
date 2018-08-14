
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import add_vectors
#from compas.geometry import distance_point_point

from compas_blender.geometry import BlenderGeometry
from compas_blender.utilities import set_select
from compas_blender.utilities import set_deselect
from compas_blender.utilities import select_mesh

try:
    import bpy
    import bmesh
except ImportError:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'BlenderMesh',
]


class BlenderMesh(BlenderGeometry):

    def __init__(self, object):
        self.guid = object.name
        self.mesh = object
        self.geometry = object.data
        self.attributes = {}
        self.otype = object.type

#    @classmethod
#    def from_selection(cls):
#        object = select_mesh()
#        return cls(object)

    @property
    def location(self):

        return list(self.mesh.location)

#    def hide(self):
#        self.mesh.hide = True

#    def show(self):
#        self.mesh.hide = False

#    def select(self):
#        self.mesh.select = True

#    def unselect(self):
#        self.mesh.select = False

    def get_vertex_coordinates(self):

        points = [list(vertex.co) for vertex in self.geometry.vertices]
        return [add_vectors(self.location, i) for i in points]

    def get_face_vertices(self):

        faces = self.get_face_vertex_indices()
        return [[list(add_vectors(self.location, self.geometry.vertices[i].co)) 
                for i in face] for face in faces]

    def get_vertex_colors(self, vertices=None):

        col = self.geometry.vertex_colors.active
        
        if col:
            colors = {}
            
            if not vertices:
                vertices = range(len(self.geometry.vertices))

            for face in self.geometry.polygons:
                for i in face.loop_indices:
                    j = self.geometry.loops[i].vertex_index
                    if (j in vertices) and (not colors.get(j, None)):
                        colors[j] = list(col.data[i].color)[:3]
                        
        return colors
        
    def set_vertex_colors(self, colors):

        if self.geometry.vertex_colors:
            col = self.geometry.vertex_colors.active
        else:
            col = self.geometry.vertex_colors.new()

        for face in self.geometry.polygons:
            for i in face.loop_indices:
                j = self.geometry.loops[i].vertex_index
                if j in colors:
                    col.data[i].color = list(colors[j]) + [1]

    def unset_vertex_colors(self):
        
        vertex_colors = self.geometry.vertex_colors 
        while vertex_colors:
            vertex_colors.remove(vertex_colors[0])

    def get_vertices_and_faces(self):

        vertices = self.get_vertex_coordinates()
        faces    = self.get_face_vertex_indices()

        return vertices, faces

    def get_border(self):

        raise NotImplementedError

    def get_vertex_index(self):

        #set_deselect()
        #set_select(objects=self.mesh)
        #bpy.ops.object.mode_set(mode='EDIT') 
        
        # USER PROMPT TO SELECT
        
        indices = []
        for i in reversed(bmesh.from_edit_mesh(self.mesh.data).select_history):
            if isinstance(i, bmesh.types.BMVert):
                indices.append(i.index)

        return indices

#    def get_face_index(self):
#        # User must be in object mode, with face selected from edit mode.
#        try:
#            return mesh.get_face_indices()[0]
#        except Exception:
#            return None

#    def get_edge_index(self):
#        # User must be in object mode, with edge selected from edit mode.
#        try:
#            return mesh.get_edge_indices()[0]
#        except Exception:
#            return None

#    def get_vertex_face_indices(self):
#        raise NotImplementedError

#    def get_vertex_indices(self):
#        # User must be in object mode, with vertices selected from edit mode.
#        return [vertex.index for vertex in self.mesh.data.vertices if vertex.select]

#    def get_edge_indices(self):
#        # User must be in object mode, with edges selected from edit mode.
#        return [edge.index for edge in self.mesh.data.edges if edge.select]

#    def get_face_indices(self):
#        # User must be in object mode, with faces selected from edit mode.
#        return [face.index for face in self.mesh.data.polygons if face.select]

#    def get_edge_vertex_indices(self):
#        return [list(edge.vertices) for edge in self.mesh.data.edges]

    def get_face_vertex_indices(self):

        return [list(face.vertices) for face in self.geometry.polygons]

#    def update_vertices(self, X):
#        for c, xyz in enumerate(list(X)):
#            self.mesh.data.vertices[c].co = xyz
#        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

#    # ==========================================================================
#    # geometric
#    # ==========================================================================

#    def normal(self, point):
#        raise NotImplementedError

#    def normals(self, points):
#        raise NotImplementedError
#        
#    def edge_length(self, edge):
#        u, v = self.mesh.data.edges[edge].vertices
#        sp, ep = [list(self.mesh.data.vertices[i].co) for i in [u, v]]
#        return distance_point_point(sp, ep)
#    
#    def edge_lengths(self):
#        return [self.edge_length(edge=i) for i in range(len(self.mesh.data.edges))]
#        
#    def face_normal(self, face):
#        return list(self.mesh.data.polygons[face].normal)

#    def face_normals(self):
#        return [list(face.normal) for face in self.mesh.data.polygons]
#    
#    def face_area(self, face):
#        return self.mesh.data.polygons[face].area

#    def face_areas(self):
#        return [face.area for face in self.mesh.data.polygons]

#    def closest_point(self, point, maxdist=None):
#        raise NotImplementedError

#    def closest_points(self, points, maxdist=None):
#        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    
    from compas_blender.utilities import get_objects


    mesh = BlenderMesh(get_objects(collection='Collection 1')[0])

    print(mesh.guid)
    print(mesh.mesh)
    print(mesh.geometry)
    print(mesh.attributes)
    print(mesh.otype)
    
#    mesh.hide()
#    mesh.show()
#    mesh.unselect()
#    mesh.select()
#    
    #print(mesh.get_vertex_coordinates())
#    print(mesh.get_edge_vertex_indices())
    #print(mesh.get_face_vertex_indices())
    #print(mesh.get_face_vertices())
    #print(mesh.get_vertices_and_faces())
    print(mesh.get_vertex_index())
#    print(mesh.face_normals())
#    print(mesh.face_normal(face=4))
#    print(mesh.face_area(face=4))
#    print(mesh.face_areas())
#    print(mesh.edge_length(edge=4))
#    print(mesh.edge_lengths())
    
    #mesh.set_vertex_colors(colors={0: [1, 0, 0], 2: [0, 1, 0], 4:[0, 0, 1]})
    #mesh.unset_vertex_colors()
    #print(mesh.get_vertex_colors(vertices=[0, 2, 4]))
    
#    X = [[x, y, z + 1] for x, y, z in mesh.get_vertex_coordinates()]
#    mesh.update_vertices(X)
#    
#    print(mesh.get_face_index())
#    print(mesh.get_edge_index())
#    print(mesh.get_vertex_index())
#    print(mesh.get_face_vertices())
