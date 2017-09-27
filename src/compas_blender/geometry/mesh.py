from compas.geometry import area_polygon
from compas.geometry import distance_point_point
from compas.geometry import normal_polygon

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'colour_bmesh_vertices',
    'bmesh_data',
    'bmesh_edge_lengths',
    'bmesh_face_areas',
    'bmesh_face_normals',
    'remove_duplicate_bmesh_vertices',
    'update_bmesh_vertices',
    'unify_bmesh_normals'
]


# ==============================================================================
# Vertices
# ==============================================================================

def colour_bmesh_vertices(bmesh, vertices, colours):
    """ Colour the vertices of a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.
        vertices (list): List of vertices to colour.
        colour (list): List of RGB colours [0, 1] based.

    Returns:
        None
    """
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
                col.data[i].color = colours[ind]
    bmesh.select = False


def remove_duplicate_bmesh_vertices(bmesh):
    """ Remove duplicate overlapping vertices of a Blender mesh object.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        obj: New Blender mesh.
    """
    bmesh.select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
    mesh = bmesh.from_edit_mesh(bpy.context.object.data)
    for vertex in mesh.verts:
        vertex.select = True
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')
    bmesh.select = False
    return mesh


def update_bmesh_vertices(bmesh, X):
    """ Update the vertex co-ordinates of a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.
        X (array, list): New x, y, z co-ordinates.

    Returns:
        None
    """
    for c, Xi in enumerate(list(X)):
        bmesh.data.vertices[c].co = Xi
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


# ==============================================================================
# Data/properties
# ==============================================================================

def bmesh_data(bmesh):
    """ Return the Blender mesh's vertices, edges and faces data.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Vertices.
        list: Edges.
        list: Faces.
    """
    vertices = [list(vertex.co) for vertex in bmesh.data.vertices]
    edges = [list(edge.vertices) for edge in bmesh.data.edges]
    faces = [list(face.vertices) for face in bmesh.data.polygons]
    return vertices, edges, faces


def bmesh_edge_lengths(bmesh):
    """ Retrieve the edge legnths of a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Lengths of each edge.
        float: Total length.
    """
    X, uv, _ = bmesh_data(bmesh)
    lengths = [distance_point_point(X[u], X[v]) for u, v in uv]
    L = sum(lengths)
    return lengths, L


def bmesh_face_areas(bmesh):
    """ Retrieve the face areas of a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Areas of each face.
        float: Total area.
    """
    vertices, edges, faces = bmesh_data(bmesh)
    polygons = [[vertices[i] for i in face] for face in faces]
    areas = [area_polygon(polygon) for polygon in polygons]
    A = sum(areas)
    return areas, A


def bmesh_face_normals(bmesh):
    """ Retrieve the face normals of a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        list: Normals of each face.
    """
    vertices, edges, faces = bmesh_data(bmesh)
    polygons = [[vertices[i] for i in face] for face in faces]
    normals = [normal_polygon(polygon) for polygon in polygons]
    return normals


def unify_bmesh_normals(bmesh):
    """ Make the Blender mesh face normals consistent.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        None
    """
    bmesh.mode_set(mode='EDIT')
    bmesh.normals_make_consistent(inside=False)
    bmesh.mode_set(mode='OBJECT')


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas_blender.utilities import draw_bmesh
    from compas_blender.utilities import clear_layers

    clear_layers([0])

    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
    faces = [[0, 1, 2], [2, 3, 0]]
    bmesh = draw_bmesh('bmesh', vertices=vertices, faces=faces, wire=True)

    colours = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]]
    colour_bmesh_vertices(bmesh, [0, 1, 2, 3], colours)

    update_bmesh_vertices(bmesh, [[0, 0, 0.1], [1, 0, 0.2], [1, 1, 0.3], [0, 1, 0]])
    
    print(bmesh_edge_lengths(bmesh))
    print(bmesh_face_areas(bmesh))
    print(bmesh_face_normals(bmesh))
