from compas.cad import MeshGeometryInterface
from compas.geometry import add_vectors
from compas_blender.utilities import select_mesh

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['BlenderMesh']


class BlenderMesh(MeshGeometryInterface):
    """"""

    def __init__(self, object):
        self.guid = object.name
        self.mesh = object
        self.geometry = None
        self.attributes = {}
        self.type = self.mesh.type

    @classmethod
    def from_selection(cls):
        object = select_mesh()
        return cls(object)

    @property
    def xyz(self):
        return list(self.mesh.location)

    def hide(self):
        self.mesh.hide = True

    def show(self):
        self.mesh.hide = False

    def select(self):
        self.mesh.select = True

    def unselect(self):
        self.mesh.select = False

    def get_vertex_coordinates(self):
        location = self.xyz
        pts_ = [list(vertex.co) for vertex in self.mesh.data.vertices]
        pts = [add_vectors(location, i) for i in pts_]
        return pts

    def get_face_vertices(self):
        raise NotImplementedError

    def get_vertex_colors(self):
        raise NotImplementedError

    def set_vertex_colors(self, vertices, colors):
        bmesh = self.mesh
        bpy.context.scene.objects.active = bmesh
        bmesh.select = True
        if bmesh.data.vertex_colors:
            col = bmesh.data.vertex_colors.active
        else:
            col = bmesh.data.vertex_colors.new()
        faces = bmesh.data.polygons
        for face in faces:
            for i in face.loop_indices:
                j = bmesh.data.loops[i].vertex_index
                if j in vertices:
                    ind = vertices.index(j)
                    col.data[i].color = colors[ind]
        bmesh.select = False

    def unset_vertex_colors(self):
        vertices = self.get_vertex_indices()
        self.set_vertex_colors(vertices, [[1, 1, 1]] * len(vertices))

    def get_vertices_and_faces(self):
        vertices = self.get_vertex_coordinates()
        faces = self.get_face_indices()
        return vertices, faces

    def get_border(self):
        raise NotImplementedError

    def get_vertex_index(self):
        raise NotImplementedError

    def get_face_index(self):
        raise NotImplementedError

    def get_vertex_face_indices(self):
        raise NotImplementedError

    def get_vertex_indices(self):
        return range(len(self.mesh.data.vertices))

    def get_edge_indices(self):
        return range(len(self.mesh.data.edges))

    def get_face_indices(self):
        return range(len(self.mesh.data.polygons))

    def get_edge_vertex_indices(self):
        return [list(edge.vertices) for edge in self.mesh.data.edges]

    def get_face_vertex_indices(self):
        return [list(face.vertices) for face in self.mesh.data.polygons]

    # ==========================================================================
    # geometric
    # ==========================================================================

    def normal(self, point):
        raise NotImplementedError

    def normals(self, points):
        raise NotImplementedError

    def closest_point(self, point, maxdist=None):
        raise NotImplementedError

    def closest_points(self, points, maxdist=None):
        raise NotImplementedError


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    mesh = BlenderMesh.from_selection()

    print(mesh.guid)
    print(mesh.mesh)
    print(mesh.geometry)
    print(mesh.attributes)
    print(mesh.type)
    print(mesh.get_vertex_coordinates())
    print(mesh.get_edge_vertex_indices())
    print(mesh.get_face_vertex_indices())
    print(mesh.get_edge_indices())
    print(mesh.get_face_indices())
    mesh.unset_vertex_colors()



# from compas.geometry import area_polygon
# from compas.geometry import distance_point_point
# from compas.geometry import normal_polygon

# def remove_duplicate_bmesh_vertices(bmesh):
#     """ Remove duplicate overlapping vertices of a Blender mesh object.

#     Parameters:
#         bmesh (obj): Blender mesh object.

#     Returns:
#         obj: New Blender mesh.
#     """
#     bmesh.select = True
#     bpy.ops.object.mode_set(mode='EDIT')
#     bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
#     mesh = bmesh.from_edit_mesh(bpy.context.object.data)
#     for vertex in mesh.verts:
#         vertex.select = True
#     bpy.ops.mesh.remove_doubles()
#     bpy.ops.object.mode_set(mode='OBJECT')
#     bmesh.select = False
#     return mesh


# def update_bmesh_vertices(bmesh, X, winswap=False):
#     """ Update the vertex co-ordinates of a Blender mesh.

#     Parameters:
#         bmesh (obj): Blender mesh object.
#         X (array, list): New x, y, z co-ordinates.
#         winswap (bool): Update workspace window.

#     Returns:
#         None
#     """
#     for c, Xi in enumerate(list(X)):
#         bmesh.data.vertices[c].co = Xi
#     if winswap:
#         bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


# def bmesh_edge_lengths(bmesh):
#     """ Retrieve the edge legnths of a Blender mesh.

#     Parameters:
#         bmesh (obj): Blender mesh object.

#     Returns:
#         list: Lengths of each edge.
#         float: Total length.
#     """
#     X, uv, _ = bmesh_data(bmesh)
#     lengths = [distance_point_point(X[u], X[v]) for u, v in uv]
#     L = sum(lengths)
#     return lengths, L


# def bmesh_face_areas(bmesh):
#     """ Retrieve the face areas of a Blender mesh.

#     Parameters:
#         bmesh (obj): Blender mesh object.

#     Returns:
#         list: Areas of each face.
#         float: Total area.
#     """
#     vertices, edges, faces = bmesh_data(bmesh)
#     polygons = [[vertices[i] for i in face] for face in faces]
#     areas = [area_polygon(polygon) for polygon in polygons]
#     A = sum(areas)
#     return areas, A


# def bmesh_face_normals(bmesh):
#     """ Retrieve the face normals of a Blender mesh.

#     Parameters:
#         bmesh (obj): Blender mesh object.

#     Returns:
#         list: Normals of each face.
#     """
#     vertices, edges, faces = bmesh_data(bmesh)
#     polygons = [[vertices[i] for i in face] for face in faces]
#     normals = [normal_polygon(polygon) for polygon in polygons]
#     return normals


# def unify_bmesh_normals(bmesh):
#     """ Make the Blender mesh face normals consistent.

#     Parameters:
#         bmesh (obj): Blender mesh object.

#     Returns:
#         None
#     """
#     bmesh.mode_set(mode='EDIT')
#     bmesh.normals_make_consistent(inside=False)
#     bmesh.mode_set(mode='OBJECT')


# def remove_duplicate_bmesh_vertices(bmesh):
#     """ Remove duplicate overlapping vertices of a Blender mesh object.

#     Parameters:
#         bmesh (obj): Blender mesh object.

#     Returns:
#         obj: New Blender mesh.
#     """
#     bmesh.select = True
#     bpy.ops.object.mode_set(mode='EDIT')
#     bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
#     mesh = bmesh.from_edit_mesh(bpy.context.object.data)
#     for vertex in mesh.verts:
#         vertex.select = True
#     bpy.ops.mesh.remove_doubles()
#     bpy.ops.object.mode_set(mode='OBJECT')
#     bmesh.select = False
#     return mesh


# def update_bmesh_vertices(bmesh, X, winswap=False):
#     """ Update the vertex co-ordinates of a Blender mesh.

#     Parameters:
#         bmesh (obj): Blender mesh object.
#         X (array, list): New x, y, z co-ordinates.
#         winswap (bool): Update workspace window.

#     Returns:
#         None
#     """
#     for c, Xi in enumerate(list(X)):
#         bmesh.data.vertices[c].co = Xi
#     if winswap:
#         bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


# def bmesh_edge_lengths(bmesh):
#     """ Retrieve the edge legnths of a Blender mesh.

#     Parameters:
#         bmesh (obj): Blender mesh object.

#     Returns:
#         list: Lengths of each edge.
#         float: Total length.
#     """
#     X, uv, _ = bmesh_data(bmesh)
#     lengths = [distance_point_point(X[u], X[v]) for u, v in uv]
#     L = sum(lengths)
#     return lengths, L


# def bmesh_face_areas(bmesh):
#     """ Retrieve the face areas of a Blender mesh.

#     Parameters:
#         bmesh (obj): Blender mesh object.

#     Returns:
#         list: Areas of each face.
#         float: Total area.
#     """
#     vertices, edges, faces = bmesh_data(bmesh)
#     polygons = [[vertices[i] for i in face] for face in faces]
#     areas = [area_polygon(polygon) for polygon in polygons]
#     A = sum(areas)
#     return areas, A


# def bmesh_face_normals(bmesh):
#     """ Retrieve the face normals of a Blender mesh.

#     Parameters:
#         bmesh (obj): Blender mesh object.

#     Returns:
#         list: Normals of each face.
#     """
#     vertices, edges, faces = bmesh_data(bmesh)
#     polygons = [[vertices[i] for i in face] for face in faces]
#     normals = [normal_polygon(polygon) for polygon in polygons]
#     return normals


# def unify_bmesh_normals(bmesh):
#     """ Make the Blender mesh face normals consistent.

#     Parameters:
#         bmesh (obj): Blender mesh object.

#     Returns:
#         None
#     """
#     bmesh.mode_set(mode='EDIT')
#     bmesh.normals_make_consistent(inside=False)
#     bmesh.mode_set(mode='OBJECT')
